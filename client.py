import grpc
import asyncio
import services_pb2
import services_pb2_grpc

import grpc
import asyncio
import services_pb2
import services_pb2_grpc

async def handle_recommendation(stub):
    response = await stub.Recommend(services_pb2.RecommendationRequest(user_id='1'))
    print("Recommendations: ", response.recommendations)

async def handle_restaurant(stub):
    response = await stub.GetRestaurants(services_pb2.RestaurantRequest(query=''))
    print("Restaurants: ", response.names)

async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        recommendation_stub = services_pb2_grpc.RecommendationServiceStub(channel)
        restaurant_stub = services_pb2_grpc.RestaurantCatalogServiceStub(channel)

        # Create tasks for both RPC calls
        task1 = asyncio.create_task(handle_recommendation(recommendation_stub))
        task2 = asyncio.create_task(handle_restaurant(restaurant_stub))

        # Wait for both tasks to complete
        await task1
        await task2

if __name__ == '__main__':
    asyncio.run(run())



# async def recommendationAndRestaurant():
#     async with grpc.aio.insecure_channel('localhost:50051') as channel:
#         recommendation_stub = services_pb2_grpc.RecommendationServiceStub(channel)
#         restaurant_stub = services_pb2_grpc.RestaurantCatalogServiceStub(channel)

#         # For concurrent execution
#         recommendation_task = recommendation_stub.Recommend(services_pb2.RecommendationRequest(user_id='1'))
#         restaurant_task = restaurant_stub.GetRestaurants(services_pb2.RestaurantRequest(query=''))

#         # Execute
#         recommendation_response, restaurant_response = await asyncio.gather(recommendation_task, restaurant_task)

#         print("Recommendations: ", recommendation_response.recommendations)
#         print("Restaurants: ", restaurant_response.names)

# if __name__ == '__main__':
#     asyncio.run(recommendationAndRestaurant())



# import grpc
# import asyncio
# import services_pb2
# import services_pb2_grpc
# from opentelemetry import trace
# from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor

# def init_tracer():
#     trace.set_tracer_provider(TracerProvider())
#     tracer_provider = trace.get_tracer_provider()
#     otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
#     span_processor = BatchSpanProcessor(otlp_exporter)
#     tracer_provider.add_span_processor(span_processor)

# async def run():
#     init_tracer()
#     GrpcInstrumentorClient().instrument()

#     async with grpc.aio.insecure_channel('localhost:50051') as channel:
#         recommendation_stub = services_pb2_grpc.RecommendationServiceStub(channel)
#         restaurant_stub = services_pb2_grpc.RestaurantCatalogServiceStub(channel)

#         recommendation_task = recommendation_stub.Recommend(services_pb2.RecommendationRequest(user_id='1'))
#         restaurant_task = restaurant_stub.GetRestaurants(services_pb2.RestaurantRequest(query=''))

#         responses = await asyncio.gather(recommendation_task, restaurant_task)

#         print("Recommendations: ", responses[0].recommendations)
#         print("Restaurants: ", responses[1].names)

# if __name__ == '__main__':
#     asyncio.run(run())