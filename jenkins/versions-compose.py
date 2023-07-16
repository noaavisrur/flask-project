#!/usr/bin/python3

import docker

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

try:
    client = docker.from_env()
    images = client.images.list()
    existing_versions = [float(image.tags[0].split(":")[1]) for image in images if image.tags and image.tags[0].startswith("noaavisrur/flask-app:")]

    print(f"Existing versions: {existing_versions}")  # Debugging line

    if existing_versions:
        latest_version = max(existing_versions)
        next_version = latest_version + 0.1
    else:
        next_version = 1.0

    next_version = f"{next_version:.1f}"
    image_name = f"noaavisrur/flask-compose:{next_version}"
    print(f"Next version: {next_version}")  # Debugging line
    client.images.build(path="/var/lib/jenkins/workspace/docker_compose_flask/flask-project/flask+DB/flask-app", tag=image_name, rm=True, pull=True)
    print(f"Successfully built image: {image_name}")
    client.images.push(repository="noaavisrur/flask-compose", tag=next_version)
    print(f"Successfully pushed image: {image_name}")
    # Tag the next version as "latest"
    latest_image_name = "noaavisrur/flask-compose:latest"
    client.images.get(image_name).tag(latest_image_name)
    print(f"Successfully tagged image as latest: {latest_image_name}")
    # Push the latest image to Docker Hub
    client.images.push(repository="noaavisrur/flask-compose", tag="latest")
    print(f"Successfully pushed latest image: {latest_image_name}")

    # Building and pushing MySQL image with the "latest" tag
    mysql_image_name = "noaavisrur/mysql-compose:latest"
    client.images.build(path="/var/lib/jenkins/workspace/docker_compose_flask/flask-project/flask+DB/db", tag=mysql_image_name, rm=True, pull=True)
    print(f"Successfully built MySQL image: {mysql_image_name}")
    client.images.push(repository="noaavisrur/mysql-compose", tag="latest")
    print(f"Successfully pushed MySQL image: {mysql_image_name}")

    delete_old_versions("noaavisrur/flask-compose", keep_latest=5)

except Exception as e:
    print(f"An error occurred: {str(e)}")
