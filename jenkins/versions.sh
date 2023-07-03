!#/usr/bin/python3

import docker
client = docker.from_env()
images = client.images.list()
existing_versions = [float(image.tags[0].split(":")[1]) for image in images if image.tags and image.tags[0].startswith("noaavisrur/flask-app:")]
if existing_versions:
    latest_version = max(existing_versions)
    next_version = latest_version + 0.1
else:
    next_version = 1.0
# Format the version number to one decimal place
next_version = f"{next_version:.1f}"
image_name = f"noaavisrur/flaskapp:{next_version}"
client.images.build(path=".", tag=image_name, rm=True, pull=True)
print(f"Successfully built image: {image_name}")
# Push the image to Docker Hub
client.images.push(repository="noaavisrur/flask-app", tag=next_version)
print(f"Successfully pushed image: {image_name}")
client.images.push(repository="noaavisrur/flask-app", tag="latest")
