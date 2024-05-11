import grpc
import asyncio
import services_pb2
import services_pb2_grpc
import logging
from typing import Callable, Awaitable
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

delaySeconds = 0.0 #0.001

# Client Side Interceptor: Introduce delay after the response is received from the server
class ClientSideDelayInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(self, delay_ms: int, service_ids: list[str]) -> None:
        self.delay_ms = delay_ms / 1000.0  # Convert milliseconds to seconds
        self.service_ids = service_ids

    async def intercept_unary_unary(
        self, continuation: Callable, client_call_details: grpc.aio.ClientCallDetails, request
    ) -> grpc.aio.Call:
        #Intercepts the unary-unary client call to introduce a delay after receiving the server's response.
        response = await continuation(client_call_details, request)
        # Check the service ID in the metadata
        service_id = next((value for key, value in client_call_details.metadata if key == 'service-id'), None)
        # print(service_id)

        if service_id in self.service_ids:
            # print(f"Introducing delay after receiving response for service {service_id} by {self.delay_ms} seconds")
            # start_sleep_time = time.perf_counter()
            await asyncio.sleep(self.delay_ms)  # Introduce an asynchronous delay after receiving the response
            # end_sleep_time = time.perf_counter()
            # actual_delay = end_sleep_time - start_sleep_time
            # print(f"Actual delay for {service_id}: {actual_delay:.6f} seconds")
        return response



# Concurrent handler for recommendation service
async def handle_recommendation(stub):
    service_id = "recommendationService"
    metadata = grpc.aio.Metadata(("service-id", service_id),)
    start_time = time.perf_counter()
    response = await stub.Recommend(services_pb2.RecommendationRequest(user_id='1'), metadata = metadata)
    end_time = time.perf_counter()
    # elapsed_time = end_time - start_time
    # print("Recommendations: ", response.recommendations)
    # print(f"Request took approximately {elapsed_time:.6f} seconds.")
    return (service_id, start_time, end_time)



# Concurrent handler for restaurant service
async def handle_restaurant(stub):
    service_id = "restaurantService"
    metadata = grpc.aio.Metadata(("service-id", service_id),)
    start_time = time.perf_counter()
    response = await stub.GetRestaurants(services_pb2.RestaurantRequest(query=''), metadata = metadata)
    end_time = time.perf_counter()
    # elapsed_time = end_time - start_time
    # print("Restaurants: ", response.names)
    # print(f"Request took approximately {elapsed_time:.6f} seconds.")
    return (service_id, start_time, end_time)




# Various modes and tunable delay
async def run(mode, delay_sec):
    # Collect timing info
    timings = []
    interceptors = [ClientSideDelayInterceptor(delay_sec*1000, ["testService1", "recommendationService"])]  # Delays processing by 5000 milliseconds = 5 seconds
    # Create a channel and add the interceptor
    async with grpc.aio.insecure_channel('localhost:50051', interceptors=interceptors) as channel:
        recommendation_stub = services_pb2_grpc.RecommendationServiceStub(channel)
        restaurant_stub = services_pb2_grpc.RestaurantCatalogServiceStub(channel)

        if mode == 'concurrent':
            # Create tasks for both RPC calls
            task1 = asyncio.create_task(handle_recommendation(recommendation_stub))
            task2 = asyncio.create_task(handle_restaurant(restaurant_stub))

            # Wait for both tasks to complete
            results = await asyncio.gather(task1, task2)
            timings.extend(results)

        elif mode == 'sequential':
            resultReco = await handle_recommendation(recommendation_stub)
            resultRest = await handle_restaurant(restaurant_stub)
            timings.append(resultReco)
            timings.append(resultRest)
    return timings



# Simple "Trace" plots
def timePlots(timings):
    labels, start_times, end_times = zip(*timings)
    start_times = np.array(start_times)
    end_times = np.array(end_times)

    plt.figure(figsize=(15, 4))
    plt.barh(labels, end_times - start_times, left=start_times, color='violet', height=0.25)
    # plot theoretical delay on top of the execution timeline
    delay_end_time = end_times[list(labels).index("recommendationService")]
    plt.barh("recommendationService", delaySeconds*0.6, left=delay_end_time - delaySeconds*0.6, color='red', height=0.25)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Services')
    plt.xlim(min(start_times)-0.0015, max(end_times)+0.0015)
    plt.title('Services Execution Timelines')
    plt.grid(True)
    plt.show()



# Distribution of the count of the first return service
def plotFirst(reco_ends_first, rest_ends_first, seq_reco, seq_rest):
    mpl.rcParams.update({'font.size': 12})

    # Labels and data
    services = ['Concurrent', 'Sequential']
    counts_reco = [reco_ends_first, seq_reco]  # Data for recommendationService
    counts_rest = [rest_ends_first, seq_rest]  # Data for restaurantService

    # Create a numpy array for the x locations for the groups
    index = np.arange(len(services))
    width = 0.4  # the width of the bars
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plotting data
    bars_reco = ax.bar(index - width/2, counts_reco, width, label='recommendationService', color='violet')
    bars_rest = ax.bar(index + width/2, counts_rest, width, label='restaurantService', color='pink')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Execution Workflow')
    ax.set_ylabel('Count')
    ax.set_title('The count of the first returning service in concurrent execution of 1000 runs')
    ax.set_xticks(index)
    ax.set_xticklabels(services)

    # Label with the exact count above each bar
    for bars in (bars_reco, bars_rest):
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # only put text if there is a height
                ax.annotate('{}'.format(height), xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),  # vertical offset
                            textcoords="offset points", ha='center', va='bottom')
    plt.legend()
    plt.show()



# Generate aggregated results
async def multiple_runs(mode, num_runs, delay):
    # Initialize lists to hold timing data
    reco_times = []
    rest_times = []
    reco_ends = []
    rest_ends = []

    for _ in range(num_runs):
        result = await run(mode, delay)
        reco_data = next(item for item in result if item[0] == "recommendationService")
        rest_data = next(item for item in result if item[0] == "restaurantService")
        reco_times.append(reco_data[2] - reco_data[1])  # reco end time - reco start time
        rest_times.append(rest_data[2] - rest_data[1])  # rest end time - rest start time
        reco_ends.append(reco_data[2])
        rest_ends.append(rest_data[2])
    
    # Calculate averages
    avg_reco_time = np.mean(reco_times)
    avg_rest_time = np.mean(rest_times)

    # Determine which service ends first
    reco_first = sum(1 for reco, rest in zip(reco_ends, rest_ends) if reco < rest)
    rest_first = len(reco_ends) - reco_first  # total runs - reco first gives rest first

    return {
        "average_reco_time": format(avg_reco_time, '.5g'),
        "average_rest_time": format(avg_rest_time, '.5g'),
        "reco_ends_first": reco_first,
        "rest_ends_first": rest_first
    }



# Delays on the x-axis versus actual service execution time
async def multiple_delays(mode, delay):
    # Initialize lists to hold timing data
    reco_times = []
    rest_times = []
    delays = np.arange(0, delay, 0.001)

    for i in delays:
        result = await run(mode, i)
        reco_data = next(item for item in result if item[0] == "recommendationService")
        rest_data = next(item for item in result if item[0] == "restaurantService")
        reco_times.append(reco_data[2] - reco_data[1])  # reco end time - reco start time
        rest_times.append(rest_data[2] - rest_data[1])  # rest end time - rest start time
    
    plt.figure(figsize=(10, 5))
    plt.scatter(delays, reco_times, c='violet', label='Recommendation Service')
    plt.plot(delays, reco_times, 'purple', alpha=0.3)
    plt.scatter(delays, rest_times, c='pink', label='Restaurant Service')
    plt.plot(delays, rest_times, 'pink', alpha=0.3)
    plt.title(f'Service response times in {mode} mode')
    plt.xlabel('Delay (s)')
    plt.ylabel('Response Time (s)')
    plt.legend()
    plt.grid(True)
    plt.show()



# The actual delay is smaller & converge to the intended delay with greater # of runs
async def precision():
    run_times = np.arange(1, 31, 1)
    con_delays = []
    seq_delays = []

    for runs in run_times:
        # Concurrent with/o delays
        con_output_nodelay = await multiple_runs('concurrent', runs, 0.0)
        con_output_delay = await multiple_runs('concurrent', runs, 0.01)
        con_actual_avg_delay = float(con_output_delay.get("average_reco_time")) - float(con_output_nodelay.get("average_reco_time"))
        con_delays.append(con_actual_avg_delay)
        # Sequential with/o delays
        seq_output_nodelay = await multiple_runs('sequential', runs, 0.0)
        seq_output_delay = await multiple_runs('sequential', runs, 0.01)
        seq_actual_avg_delay = float(seq_output_delay.get("average_reco_time")) - float(seq_output_nodelay.get("average_reco_time"))
        seq_delays.append(seq_actual_avg_delay)
            
    plt.figure(figsize=(10, 5))
    plt.scatter(run_times, con_delays, c='violet')
    plt.plot(run_times, con_delays, 'violet', label='Concurrent Average Delay')
    plt.scatter(run_times, seq_delays, c='pink')
    plt.plot(run_times, seq_delays, 'pink', label='Sequential Average Delay')
    plt.title('Average Actual Delay by Execution Type')
    plt.xlabel('Run Times')
    plt.ylabel('Average Delay (s)')
    plt.legend()
    plt.grid(True)
    plt.show()



# Main func
if __name__ == '__main__':
    try:
        mode = int(input("Select a mode (0 -> concurrent, 1 -> sequential): "))
        if mode == 0:
            timings = asyncio.run(run('concurrent', delaySeconds))
            timePlots(timings) 
        elif mode == 1:
            timings = asyncio.run(run('sequential', delaySeconds))
            timePlots(timings) 
        elif mode == 2:
            runs = 10
            # Concurrent with/o delays
            con_output_nodelay = asyncio.run(multiple_runs('concurrent', runs, 0.0))
            print("Concurrent No Delay", con_output_nodelay)
            con_output_delay = asyncio.run(multiple_runs('concurrent', runs, 0.01))
            print("Concurrent With Delay", con_output_delay)
            con_actual_avg_delay = float(con_output_delay.get("average_reco_time")) - float(con_output_nodelay.get("average_reco_time"))
            print("The actual average delay in concurrent execution is", con_actual_avg_delay)
            # Sequential with/o delays
            seq_output_nodelay = asyncio.run(multiple_runs('sequential', runs, 0.0))
            print("Sequential No Delay", seq_output_nodelay)
            seq_output_delay = asyncio.run(multiple_runs('sequential', runs, 0.01))
            print("Sequential With Delay", seq_output_delay)
            seq_actual_avg_delay = float(seq_output_delay.get("average_reco_time")) - float(seq_output_nodelay.get("average_reco_time"))
            print("The actual average delay in sequential execution is", seq_actual_avg_delay)
            # plotFirst(con_output_nodelay.get("reco_ends_first"), con_output_nodelay.get("rest_ends_first"), seq_output_nodelay.get("reco_ends_first"), seq_output_nodelay.get("rest_ends_first"))
        elif mode == 3: #overhead
            asyncio.run(multiple_delays('concurrent',0.1))
            asyncio.run(multiple_delays('sequential',0.1))
        elif mode == 4: #precision
            asyncio.run(precision())
        else:
            raise ValueError("Invalid Input!!! Please choose 0 for concurrent or 1 for sequential mode!")
    except ValueError as e:
        print(f"Error: {e}")