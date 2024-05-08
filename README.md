# delay-gRPC-demo

Keep a copy of my master thesis

## Commands
* Generate stubs of gRPC in Python

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services.proto
```

## Notes
* Make sure all servers listening on port 50051 are properly terminated!!!


## Python
* [gRPC Interceptors](https://grpc.github.io/grpc/python/grpc_asyncio.html#grpc.aio.ClientInterceptor)
* Challenge: Global Interpreter Lock (GIL)
