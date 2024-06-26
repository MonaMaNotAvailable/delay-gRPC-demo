# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import services_pb2 as services__pb2


class RecommendationServiceStub(object):
    """The recommendation service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Recommend = channel.unary_unary(
                '/demo.RecommendationService/Recommend',
                request_serializer=services__pb2.RecommendationRequest.SerializeToString,
                response_deserializer=services__pb2.RecommendationResponse.FromString,
                )


class RecommendationServiceServicer(object):
    """The recommendation service definition.
    """

    def Recommend(self, request, context):
        """Sends a greeting
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RecommendationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Recommend': grpc.unary_unary_rpc_method_handler(
                    servicer.Recommend,
                    request_deserializer=services__pb2.RecommendationRequest.FromString,
                    response_serializer=services__pb2.RecommendationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'demo.RecommendationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RecommendationService(object):
    """The recommendation service definition.
    """

    @staticmethod
    def Recommend(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/demo.RecommendationService/Recommend',
            services__pb2.RecommendationRequest.SerializeToString,
            services__pb2.RecommendationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class RestaurantCatalogServiceStub(object):
    """The restaurant catalog service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetRestaurants = channel.unary_unary(
                '/demo.RestaurantCatalogService/GetRestaurants',
                request_serializer=services__pb2.RestaurantRequest.SerializeToString,
                response_deserializer=services__pb2.RestaurantResponse.FromString,
                )


class RestaurantCatalogServiceServicer(object):
    """The restaurant catalog service definition.
    """

    def GetRestaurants(self, request, context):
        """Fetch restaurant data
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RestaurantCatalogServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetRestaurants': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRestaurants,
                    request_deserializer=services__pb2.RestaurantRequest.FromString,
                    response_serializer=services__pb2.RestaurantResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'demo.RestaurantCatalogService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RestaurantCatalogService(object):
    """The restaurant catalog service definition.
    """

    @staticmethod
    def GetRestaurants(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/demo.RestaurantCatalogService/GetRestaurants',
            services__pb2.RestaurantRequest.SerializeToString,
            services__pb2.RestaurantResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
