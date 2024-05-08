import grpc
import asyncio
import services_pb2
import services_pb2_grpc
import logging
from typing import Callable, Awaitable
import time

class ClientSideDelayInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(self, delay_ms: int, service_ids: list[str]) -> None:
        #The delay is introduced after the response is received from the server
        self.delay_ms = delay_ms / 1000.0  # Convert milliseconds to seconds
        self.service_ids = service_ids

    async def intercept_unary_unary(
        self, continuation: Callable, client_call_details: grpc.aio.ClientCallDetails, request
    ) -> grpc.aio.Call:
        #Intercepts the unary-unary client call to introduce a delay after receiving the server's response.
        
        response = await continuation(client_call_details, request)
        
        # Check the service ID in the metadata
        service_id = next((value for key, value in client_call_details.metadata if key == 'service-id'), None)
        print(service_id)

        if service_id in self.service_ids:
            logging.info(f"Introducing delay after receiving response for service {service_id} by {self.delay_ms} seconds")
            await asyncio.sleep(self.delay_ms)  # Introduce an asynchronous delay after receiving the response
        return response

async def handle_recommendation(stub):
    service_id = "recommendationService"
    metadata = grpc.aio.Metadata(("service-id", service_id),)
    start_time = time.time()
    response = await stub.Recommend(services_pb2.RecommendationRequest(user_id='1'), metadata = metadata)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Recommendations: ", response.recommendations)
    print(f"Request took approximately {elapsed_time:.6f} seconds.")

async def handle_restaurant(stub):
    service_id = "restaurantService"
    metadata = grpc.aio.Metadata(("service-id", service_id),)
    start_time = time.time()
    response = await stub.GetRestaurants(services_pb2.RestaurantRequest(query=''), metadata = metadata)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Restaurants: ", response.names)
    print(f"Request took approximately {elapsed_time:.6f} seconds.")

async def run(mode):
    interceptors = [
        ClientSideDelayInterceptor(0, ["testService1", "recommendationService"])  # Delays processing by 5000 milliseconds = 5 seconds
    ]
    async with grpc.aio.insecure_channel('localhost:50051', interceptors=interceptors) as channel:
        recommendation_stub = services_pb2_grpc.RecommendationServiceStub(channel)
        restaurant_stub = services_pb2_grpc.RestaurantCatalogServiceStub(channel)

        if mode == 'concurrent':
            # Create tasks for both RPC calls
            task1 = asyncio.create_task(handle_recommendation(recommendation_stub))
            task2 = asyncio.create_task(handle_restaurant(restaurant_stub))

            # Wait for both tasks to complete
            await asyncio.gather(task1, task2)
            # await task1
            # await task2

        elif mode == 'sequential':
            await handle_recommendation(recommendation_stub)
            await handle_restaurant(restaurant_stub)

if __name__ == '__main__':
    try:
        mode = int(input("Select a mode (0 -> concurrent, 1 -> sequential): "))
        if mode == 0:
            asyncio.run(run('concurrent'))
        elif mode == 1:
            asyncio.run(run('sequential'))
        else:
            raise ValueError("Invalid Input!!! Please choose 0 for concurrent or 1 for sequential mode!")
    except ValueError as e:
        print(f"Error: {e}")