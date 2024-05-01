# delay-gRPC-demo

Keep a copy of my master thesis

## Commands
* Generate stubs of gRPC  

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services.proto
```

## Notes
* Make sure all servers listening on port 50051 are properly terminated!!!