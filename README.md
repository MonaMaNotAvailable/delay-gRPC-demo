# Teasing Out Causal Relationships in Distributed Systems by Adding Delays to gRPCs

Keep a copy of my master project toy demo

## Slides
You can view the final presentation slides [here](./FinalPresentation.pdf).

## Commands
* Generate stubs of gRPC in Python

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services.proto
```

## Notes
* Make sure all servers listening on port 50051 are properly terminated!!!


## Python Dependencies
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [gRPC Interceptors](https://grpc.github.io/grpc/python/grpc_asyncio.html#grpc.aio.ClientInterceptor)
* Limitation: [Global Interpreter Lock (GIL)](https://wiki.python.org/moin/GlobalInterpreterLock)

## Abstract
This research project explores the potential of introducing delays into gRPC calls to uncover causal relationships and dependencies within distributed systems. Despite the widespread adoption of microservices in modern software architecture, which often operates under complex sequential, concurrent, and parallel processes to enhance scalability, their interdependencies remain ambiguously defined. By strategically inserting delays, this study offers a novel approach to trace and clarify these interactions, which are critical for optimizing system performance and reliability. The findings provide valuable insights into system behaviors, enabling targeted optimizations for crucial system components and potentially leading to significant enhancements in overall system efficiency. The methodology advocates a shift from traditional passive observation techniques to an active perturbation approach, facilitating a deeper understanding of the dynamics of microservices in distributed systems.