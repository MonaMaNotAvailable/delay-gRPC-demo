import grpc
from concurrent import futures
import services_pb2
import services_pb2_grpc
import asyncio

class RecommendationService(services_pb2_grpc.RecommendationServiceServicer):
    async def Recommend(self, request, context):
        # await asyncio.sleep(3)  # simulate delay
        recommendations = ['Pasta', 'KoreanBBQ', 'Okonomiyaki'] 
        return services_pb2.RecommendationResponse(recommendations=recommendations)

class RestaurantCatalogService(services_pb2_grpc.RestaurantCatalogServiceServicer):
    async def GetRestaurants(self, request, context):
        # await asyncio.sleep(1)  # simulate delay
        restaurants = ['Carmelina', 'Naksan', 'Ittoku'] 
        return services_pb2.RestaurantResponse(names=restaurants)

async def serve():
    server = grpc.aio.server()
    services_pb2_grpc.add_RecommendationServiceServicer_to_server(RecommendationService(), server)
    services_pb2_grpc.add_RestaurantCatalogServiceServicer_to_server(RestaurantCatalogService(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())

# import grpc
# from concurrent import futures
# import services_pb2
# import services_pb2_grpc
# import asyncio
# from opentelemetry import trace
# from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor

# def init_tracer():
#     # Set up the tracer provider and processor
#     trace.set_tracer_provider(TracerProvider())
#     tracer_provider = trace.get_tracer_provider()

#     # Configure the OTLP exporter and connect it to a span processor
#     otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
#     span_processor = BatchSpanProcessor(otlp_exporter)
#     tracer_provider.add_span_processor(span_processor)

# class RecommendationService(services_pb2_grpc.RecommendationServiceServicer):
#     async def Recommend(self, request, context):
#         await asyncio.sleep(2)
#         recommendations = ['Pizza', 'Burger', 'Sushi']
#         return services_pb2.RecommendationResponse(recommendations=recommendations)

# class RestaurantCatalogService(services_pb2_grpc.RestaurantCatalogServiceServicer):
#     async def GetRestaurants(self, request, context):
#         await asyncio.sleep(1)
#         restaurants = ['The Pizza Place', 'Burger Corner', 'Sushi World']
#         return services_pb2.RestaurantResponse(names=restaurants)

# async def serve():
#     init_tracer()
#     server = grpc.aio.server()
#     GrpcInstrumentorServer().instrument(server=server)

#     services_pb2_grpc.add_RecommendationServiceServicer_to_server(RecommendationService(), server)
#     services_pb2_grpc.add_RestaurantCatalogServiceServicer_to_server(RestaurantCatalogService(), server)
#     listen_addr = '[::]:50051'
#     server.add_insecure_port(listen_addr)
#     await server.start()
#     await server.wait_for_termination()

# if __name__ == '__main__':
#     asyncio.run(serve())