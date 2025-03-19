Following GCP documentation: 
[GCP documentation for creating a task queue](https://cloud.google.com/tasks/docs/add-task-queue)
[GCP documentation for creating a target task](https://cloud.google.com/tasks/docs/creating-http-target-tasks)
[ChatGPT chat](https://chatgpt.com/share/67dab6c7-f3d0-800c-8525-b3034b64e09e)
[Stackoverflow about docker platform on M1](https://stackoverflow.com/questions/55662222/container-failed-to-start-failed-to-start-and-then-listen-on-the-port-defined-b)

This project aims to create a python snippet that pushes a HTTP task to a cloud task queue.
This task should then be picked up and processed, returning the outcome to the user/add the outcome to a db

1. created a queue
gcloud tasks queues create my-task-queue \
    --log-sampling-ratio=1.0 \
    --location=europe-west2 \
    --project=async-link-checker
2. create main.py
3. create dockerfile
4. create requirements.txt
5. Build the container image
docker build --platform linux/amd64 -t gcr.io/async-link-checker/async-task-handler .
6. push the image
docker push gcr.io/async-link-checker/async-task-handler
6.1. this geve me: denied: Unauthenticated request. Unauthenticated requests do not have permission "artifactregistry.repositories.uploadArtifacts" on resource "projects/async-link-checker/locations/us/repositories/gcr.io" (or it may not exist)
To fix this i had to authenticate docker with gcloud
COMMAND: gcloud auth configure-docker
6.2 got error: ERROR: (gcloud.run.deploy) Revision 'async-task-handler-00002-p29' is not ready and cannot serve traffic. The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable within the allocated timeout. This can happen when the container port is misconfigured or if the timeout is too short. The health check timeout can be extended. Logs for this revision might contain more information.
enabled container registory
COMMAND: gcloud services enable containerregistry.googleapis.com
7. deploy to cloud run 
gcloud run deploy async-task-handler \
    --image gcr.io/async-link-checker/async-task-handler \
    --region europe-west2 \
    --platform managed \
    --allow-unauthenticated



Creating a task in CLI

gcloud tasks create-http-task \
    --queue=my-task-queue \
    --url=https://async-task-handler-319415279837.europe-west2.run.app/task-handler \
    --method=POST \
    --payload='{"url": "https://example.com"}' \
    --location=europe-west2 \
    --project=async-link-checker
