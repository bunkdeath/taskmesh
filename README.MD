# TaskMesh  

**TaskMesh** is a cloud-agnostic task processing framework designed to integrate seamlessly with various cloud messaging services. The initial release supports **Google Cloud Pub/Sub**, with planned support for **AWS SQS** and **Azure Service Bus**. TaskMesh simplifies distributed task execution, ensuring scalability and reliability across multiple cloud providers.

The idea behind this project is to mimic some level level of celery tasks.

The limitation: this only works for a function not on the class methods.

## Features  
✅ Google Cloud Pub/Sub\
✅ AWS SQS\
🚧 Azure Service Bus (Ongoing development)\
⬜ RabbitMQ (Planned)\
⬜ Kafka (Planned)

## Usage

This package is used specially on micro-service architecture, where we need to pass message between services.


In the examples folder, there are files for each provider. The file accept argument in command line. `--subscribe <topic>` and no argument.

Providing `--subscribe <topic>` will subscribe to the topic provided in command line and will process messages and call the desired function.

The no argument will call the function directly and delayed. The delayed call will utilize message broker for the respective provider


### Publisher Instance

```bash
python examples/aws.py
python examples/gcp.py
```

### Listener Instance

```bash
python examples/gcp.py taskmesh-sub
python examples/aws.py taskmesh
```

Note: gcp uses subscription id and aws use topic name

This will create instance that listens to the messages on the message broker and process it by calling the desired function.
