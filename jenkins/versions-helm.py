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
    for tag in image.tags:
        if tag.startswith("noaavisrur/flask-compose:"):
            try:
                left, right = map(int, tag.split(":")[1].split("."))
                left_versions.append(left)
                right_versions.append(right)
            except ValueError:
                print(f"Skipping invalid tag: {tag}")

if left_versions:
    next_version_left = max(left_versions)
    next_version_right = max(right_versions) + 1
    if next_version_right == 10:
        next_version_left += 1
        next_version_right = 0
else:
    next_version_left, next_version_right = 1, 0

next_version = f"{next_version_left}.{next_version_right}"

# Your build, push, and clean-up code can follow here
