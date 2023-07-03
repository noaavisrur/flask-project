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
existing_versions = [float(image.tags[0].split(":")[1]) for image in images if image.tags and image.tags[0].startswith("noaavisrur/flask-app:")]
if existing_versions:
    latest_version = max(existing_versions)
    next_version = latest_version + 0.1
else:
    next_version = 1.0

next_version = f"{next_version:.1f}"
image_name = f"noaavisrur/flaskapp:{next_version}"
client.images.build(path="./flask-app", tag=image_name, rm=True, pull=True)
print(f"Successfully built image: {image_name}")
client.images.push(repository="noaavisrur/flask-app", tag=next_version)
print(f"Successfully pushed image: {image_name}")
client.images.build(path="./flask-app", tag="latest", rm=True, pull=True)
print(f"Successfully built image: {image_name}")
client.images.push(repository="noaavisrur/flask-app", tag="latest")
print(f"Successfully pushed image: {image_name}")

delete_old_versions("noaavisrur/flask-app", keep_latest=5)
