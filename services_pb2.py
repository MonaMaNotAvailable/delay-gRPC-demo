# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: services.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eservices.proto\x12\x04\x64\x65mo\"(\n\x15RecommendationRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"1\n\x16RecommendationResponse\x12\x17\n\x0frecommendations\x18\x01 \x03(\t\"\"\n\x11RestaurantRequest\x12\r\n\x05query\x18\x01 \x01(\t\"#\n\x12RestaurantResponse\x12\r\n\x05names\x18\x01 \x03(\t2_\n\x15RecommendationService\x12\x46\n\tRecommend\x12\x1b.demo.RecommendationRequest\x1a\x1c.demo.RecommendationResponse2_\n\x18RestaurantCatalogService\x12\x43\n\x0eGetRestaurants\x12\x17.demo.RestaurantRequest\x1a\x18.demo.RestaurantResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_RECOMMENDATIONREQUEST']._serialized_start=24
  _globals['_RECOMMENDATIONREQUEST']._serialized_end=64
  _globals['_RECOMMENDATIONRESPONSE']._serialized_start=66
  _globals['_RECOMMENDATIONRESPONSE']._serialized_end=115
  _globals['_RESTAURANTREQUEST']._serialized_start=117
  _globals['_RESTAURANTREQUEST']._serialized_end=151
  _globals['_RESTAURANTRESPONSE']._serialized_start=153
  _globals['_RESTAURANTRESPONSE']._serialized_end=188
  _globals['_RECOMMENDATIONSERVICE']._serialized_start=190
  _globals['_RECOMMENDATIONSERVICE']._serialized_end=285
  _globals['_RESTAURANTCATALOGSERVICE']._serialized_start=287
  _globals['_RESTAURANTCATALOGSERVICE']._serialized_end=382
# @@protoc_insertion_point(module_scope)