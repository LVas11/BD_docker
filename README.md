# Weather forecast tool (Dockerized)

The python project is a simple command-line application that generates current weather conditions and a 24-hour forecast for user provided city. 
The forecast is presented in a graph format for each hour and saved as a .png file. 


**Files:** 
 - weather.py: main python code for the CLI application
 - weather_codes.json: contains keys of weather codes used by the weather tool
 - requirements.txt: dependencies required for the python code
 - Dockerfile: contains instructions to build the Docker image.


**Contents of the Docker file:**
- *Base image:* specifies Python 3.9 slim base image to limit image size;
- *Workspace:* sets /app as primary directory
- *Environment* settings: sets PYTHONUNBUFFERED=1 to ensure prompts appear in terminal without buffer
- *Dependecies:* copies dependencies from requirements.txt file; installs them
- *App code:* copied the application code and .json file


**Steps followed to create the Docker image:**
- Created Dockerfile as described above. 
- From the Dockerfile the image was created by running the below comand in terminal:
  ```docker build -t weather-tool:v1 .```
- Running the container by the below command. NOTE: since the weather tool requires user input, it is run in interactive terminal (-it):
  ``` docker run -it --rm -v ${PWD}:/app weather-tool:v1 ```
- The forecast graph forecast_XCITY.png file is then saved locally in working directory
- Docker image was pushed to registry (Docker Hub). Image tag: lvas55/weather-tool:latest

**Image tag**:  ```lvas55/weather-tool:latest ```
The project can be run via docker: ```-it -v ${PWD}:/app lvas55/weather-tool:latest```


**Issues and notes:**

Two main issue were encountered in the process of making Docker image and running the container:

- During the container creation process, a version mismatch was identified for mathplotlib library.
It appears that the specified version that was on the local Windows environment was not available to Linux-based python:3.9-slim Docker image.
So a minimum compatible version was specified (>= 3.8.0) instead of the strictly the same version.
- Since the file request user input, the container does not run smoothly in docker.desktop app (does not wait for input and stops running immediately).
The solution here is to run it via the terminal, as described above. Works as expected then.

 






