import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from taskmesh import Task
from taskmesh.config import Config
from taskmesh.providers.gcp import GCPProvider, Subscriber

PROJECT_ROOT = Path(__file__).resolve().parent
use_file = False


if use_file:
    # using file withoug using the environment variable
    gcp_secret_file = os.path.join(PROJECT_ROOT, ".secret/gcp-key.json")
    gcp = GCPProvider(credential_file=gcp_secret_file, project_id="task-mesh")
else:
    # using file with environment variable
    load_dotenv()
    gcp = GCPProvider(project_id=os.environ.get("GCP_PROJECT_ID"))


config = Config()
# # setting false will bypass the background task. The funciton will be called directly
# config.background_task_status(False)

task = Task(provider=gcp, config=config)


@task.listen(topic="taskmesh")
def hello_world(msg, counter):
    print(f"Hello World from {msg} - {counter}")


def setup_config():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process provider, subscribe, and publish options."
    )

    # Add mutually exclusive group for subscribe and publish
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--subscribe",
        "-s",
        type=str,
        help="Specify the subscribe topic name (string).",
    )
    group.add_argument(
        "--publish",
        "-p",
        action="store_true",
        help="Enable publishing (no value needed).",
    )

    return parser


def parse_args(parser):
    # Parse arguments
    args = parser.parse_args()

    # Access the arguments
    subscribe = args.subscribe

    if subscribe:
        print(f"GCP: Subscribing to {subscribe}")
        sub = Subscriber(provider=gcp, config=config, subscription_name=subscribe)
        sub.start_listening()
    else:
        for i in range(10):
            hello_world("Direct call", i)
            hello_world.delay("Delayed call", i)


if __name__ == "__main__":
    parser = setup_config()
    parse_args(parser)
