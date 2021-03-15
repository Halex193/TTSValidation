# set base image (host OS)
FROM borda/docker_python-opencv-ffmpeg:cpu-py3.9-cv4.5.1

# install build-essential
RUN apt -y update && apt -y install build-essential

# Upgrade pip
RUN /usr/bin/python3.9 -m pip install --upgrade pip

# set the working directory in the container
WORKDIR /project

# install dependencies
RUN pip install pybind11
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .
COPY files files

# command to run on container start
CMD [ "python3", "./tests.py" ]