# TaskMesh  

**TaskMesh** is a cloud-agnostic task processing framework designed to integrate seamlessly with various cloud messaging services. The initial release supports **Google Cloud Pub/Sub**, with planned support for **AWS SQS** and **Azure Service Bus**. TaskMesh simplifies distributed task execution, ensuring scalability and reliability across multiple cloud providers.

The idea behind this project is to mimic some level level of celery tasks. 

## Features  
✅ Google Cloud Pub/Sub\
🚧 AWS SQS (Coming Soon)\
⬜ Azure Service Bus (Coming Soon)\
⬜ RabbitMQ (Planned)\
⬜ Kafka (Planned)

## Usage

This package is used specially on micro-service architecture, where we need to pass message between services.

Hence two instance of example.py needs to be run.

### Publisher Instance

Here we run the `example.py` file without any argument. This will call the function 10 times my passing message to message broker and calling function directly.

### Listener Instance

Here, we listen to the messages on the message broker and process the message by calling the function which was delayed called. To run the Listener Instance, run the `example.py` file by providing subscription name as arguments. e.g. 
```bash
python example.py task-mesh-sub
```

This will create instance that listens to the messages on the message broker and process it by calling the desired function.