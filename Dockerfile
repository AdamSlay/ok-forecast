# Dockerfile - blueprint for docker image

# from image:tag
FROM python:3.10

# add source, destination (. = current dir)
ADD src/forecast.py .
ADD src/forecast_api.py .

# copy source, origin
COPY requirements.txt .

# copy data
COPY data /data

# run command, '--no-cache-dir' to remove install files(*.tar.gz and other such files)
# this helps keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# CMD to run when the container is opened
CMD ["python3", "./forecast.py"]

# run the following cmd in the terminal to build this dockerfile:
# docker build -t python-async .
# -t gives the build a tag. in this case "python-async"
# . means build from current directory