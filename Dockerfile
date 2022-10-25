# Dockerfile - blueprint for docker image

# from image:tag
FROM python:3.10


# copy source, origin
COPY requirements.txt .

# get the geopandas requirements from apt before installing with pip
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libatlas-base-dev \
  libgdal-dev \
  gfortran


# run command, '--no-cache-dir' to remove install files(*.tar.gz and other such files)
# this helps keep the image small
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home forecast-user
WORKDIR /home/forecast-user
USER forecast-user

COPY data data/
COPY src/forecast.py .
COPY src/forecast_api.py .
COPY src/forecast_plot.py .

# CMD to run when the container is opened
CMD ["python3", "forecast.py"]
