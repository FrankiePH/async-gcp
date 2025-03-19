import json
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import datetime

def create_task(project, location, queue, handler_url, target_url, task_name):
    # Create a Cloud Tasks client.
    client = tasks_v2.CloudTasksClient()

    # Build the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Prepare the payload that will be sent to your task handler.
    payload = json.dumps({"url": target_url}).encode()

    # Construct the task.
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": handler_url,
            "headers": {"Content-Type": "application/json"},
            "body": payload,
        },
        "name": task_name
    }


    # Optionally, specify a task name (must be in full resource format).
    # If you want to schedule the task a few seconds in the future, you can do so.
    # For immediate execution, you can skip this.
    # schedule_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
    # timestamp = timestamp_pb2.Timestamp()
    # timestamp.FromDatetime(schedule_time)
    # task["schedule_time"] = timestamp

    # Create the task.
    response = client.create_task(request={"parent": parent, "task": task})
    print("Task created:", response.name)


if __name__ == "__main__":
    project = "async-link-checker"
    location = "europe-west2"
    queue = "my-task-queue"
    handler_url = "https://async-task-handler-319415279837.europe-west2.run.app/task-handler"
    target_url = "https://example.com"  # The URL you want your task handler to GET.
    task_name = 'projects/async-link-checker/locations/europe-west2/queues/my-task-queue/tasks/task-133'


    create_task(project, location, queue, handler_url, target_url, task_name)
