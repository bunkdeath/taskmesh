import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from taskmesh import Task
from taskmesh.config import Config
from taskmesh.providers.gcp import GCPProvider, Subscriber

PROJECT_ROOT = Path(__file__).resolve().parent
use_file = True


if use_file:
    # using file withoug using the environment variable
    gcp_secret_file = os.path.join(PROJECT_ROOT, ".secret/gcp-key.json")
    gcp = GCPProvider(credential_file=gcp_secret_file, project_id="task-mesh")
else:
    # using file with environment variable
    load_dotenv()
    gcp = GCPProvider(project_id=os.environ.get("GCP_PROJECT_ID"))


config = Config()
# config.background_task_status(False)

task = Task(provider=gcp, config=config)


@task.listen(topic="taskmesh")
def hello_world(msg, counter):
    print(f"Hello World from {msg} - {counter}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        subscription_name = sys.argv[1]
        print(f"listening to taskmesh {subscription_name}")
        sub = Subscriber(
            provider=gcp, config=config, subscription_name=subscription_name
        )
        sub.start_listening()
    else:
        for i in range(10):
            hello_world("Direct call", i)
            hello_world.delay("Delayed call", i)
    print("done")
