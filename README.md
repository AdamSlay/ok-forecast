# Oklahoma Hourly Forecast Map
This is a simple Forecast Map using weather data from Weather.gov to display hourly forecast data in Oklahoma.
My primary goals with this project were to utilize asynchronous programing and Docker. 

## Running the program
To build the Docker image, clone the repo then execute the following command while in the project directory:
```bash
docker build -t ok-forecast .
```
then, to run the container, execute the following command:
```bash
docker run --rm -v ${PWD}/maps:/home/forecast-user/maps ok-forecast
```
This command creates a new directory called ```maps``` in your local working directory
and mounts it to the container. Then it runs the forecast script inside the container. This allows the map ```.png``` files to be
saved on your machine. 