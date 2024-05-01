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
