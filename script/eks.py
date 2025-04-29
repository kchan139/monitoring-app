import os
from dotenv import load_dotenv
from kubernetes import client, config

# Load image URI from local .env
load_dotenv()
image_uri = os.getenv('IMAGE_URI')
if not image_uri:
    print("Error: IMAGE_URI environment variable not set.")
    exit(1)

# Load kubernetes configuraion
config.load_kube_config()

# Create a kubernetes API client
api_client = client.ApiClient()

deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="monitoring-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "monitoring-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "monitoring-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="monitoring-app",
                        image=image_uri,
                        ports=[client.V1ContainerPort(container_port=8080)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "monitoring-app"},
        ports=[client.V1ServicePort(port=8080)]
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)