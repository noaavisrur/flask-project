import docker
import os
from docker.errors import DockerException

def delete_old_versions(image_name, keep_latest=5):
    client = docker.from_env()
    images = client.images.list(name=image_name)

    if len(images) <= keep_latest:
        return

    images.sort(key=lambda image: image.attrs["Created"], reverse=True)

    for i in range(keep_latest, len(images)):
        image = images[i]
        for tag in image.tags:
            if tag.startswith(image_name + ":"):
                print(f"Deleting image: {tag}")
                client.images.remove(image=tag, force=True)

# Specify the path to the directory containing the docker-compose.yml file
compose_path = "/var/lib/jenkins/workspace/docker_compose_flask/flask-project/flask+DB"

# Change to the directory containing the docker-compose.yml file
os.chdir(compose_path)

# Get the latest version
client = docker.from_env()
existing_versions = [float(tag.split(":")[1]) for image in client.images.list() for tag in image.tags if tag.startswith("noaavisrur/flask-compose:")]
if existing_versions:
    latest_version = max(existing_versions)
    next_version = latest_version + 0.1
else:
    next_version = 1.0

# Format the version number
next_version = f"{next_version:.1f}"

# Build and push the Docker Compose project
image_name = f"noaavisrur/flask-compose:{next_version}"
latest_image_name = "noaavisrur/flask-compose:latest"

client.images.build(path=compose_path, tag=image_name)
client.images.push(repository="noaavisrur/flask-compose", tag=next_version)

# Tag the next version as "latest"
client.images.get(image_name).tag(latest_image_name)

# Push the latest image to Docker Hub
client.images.push(repository="noaavisrur/flask-compose", tag="latest")

delete_old_versions("noaavisrur/flask-compose", keep_latest=5)
