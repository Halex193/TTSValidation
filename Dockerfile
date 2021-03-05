# set base image (host OS)
FROM borda/docker_python-opencv-ffmpeg:cpu-py3.9-cv4.5.1

# set the working directory in the container
WORKDIR /project

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .
COPY files/data.txt files/data.txt

# command to run on container start
CMD [ "python3", "./tests.py" ]