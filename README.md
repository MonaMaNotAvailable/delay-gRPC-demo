# delay-gRPC-demo

Keep a copy of my master project

## Commands
* Generate stubs of gRPC in Python

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services.proto
```

## Notes
* Make sure all servers listening on port 50051 are properly terminated!!!


## Python
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [gRPC Interceptors](https://grpc.github.io/grpc/python/grpc_asyncio.html#grpc.aio.ClientInterceptor)
* Limitation: [Global Interpreter Lock (GIL)](https://wiki.python.org/moin/GlobalInterpreterLock)
