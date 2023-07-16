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

client = docker.from_env()
images = client.images.list()

left_versions = []
right_versions = []
for image in images:
    if image.tags and image.tags[0].startswith("noaavisrur/flask-compose:"):
        left, right = map(int, image.tags[0].split(":")[1].split("."))
        left_versions.append(left)
        right_versions.append(right)

if left_versions:
    latest_left_version = max(left_versions)
    latest_right_version = max(right_versions)
    next_version = f"{latest_left_version}.{latest_right_version + 1}"
else:
    next_version = "1.0"

image_name = f"noaavisrur/flask-compose:{next_version}"
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
