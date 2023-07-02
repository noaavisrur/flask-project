FROM python:3.8

# set a directory for the app
WORKDIR /var/lib/jenkins/workspace/docker_flask_project/flask_project/flask-app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./app.py"]
