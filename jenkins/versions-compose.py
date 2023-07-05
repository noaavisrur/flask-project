#!/usr/bin/python3

import os
import subprocess

def delete_old_versions(image_name, keep_latest=5):
    # Docker image deletion logic (same as before)
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

# Step 1: Build and run containers using docker-compose
compose_command = "docker-compose -f /var/lib/jenkins/workspace/docker_compose_flask/flask-project/flask+DB/docker-compose.yml up --build -d"
subprocess.run(compose_command, shell=True, check=True)

# Step 2: Get the version information and calculate the next version
# (same as before)

# Step 3: Tag and push the Flask image
image_name = f"noaavisrur/flask-app:{next_version}"
latest_image_name = "noaavisrur/flask-app:latest"

# Tag the next version
tag_command = f"docker tag {image_name} {latest_image_name}"
subprocess.run(tag_command, shell=True, check=True)

# Push the tagged images
push_command = f"docker push {image_name}"
subprocess.run(push_command, shell=True, check=True)
push_command = f"docker push {latest_image_name}"
subprocess.run(push_command, shell=True, check=True)

# Step 4: Delete old versions
delete_old_versions("noaavisrur/flask-app", keep_latest=5)
