# United States Hourly Forecast Map
This is a simple Forecast Map using station info from [Meteostat](https://dev.meteostat.net/python/daily.html#example) and weather data from [Weather.gov](https://weather-gov.github.io/api/general-faqs) to display hourly forecast data
for each state in the continental United States.
My primary goals with this project were to utilize asynchronous programing and Docker containerization while build skills in data visualization. 

## Running the program
To build the Docker image, clone the repo then execute the following command while in the project directory:
```bash
docker build -t us-forecast .
```
then, to run the container, execute the following command:
```bash
docker run --rm -v ${PWD}/maps:/home/forecast-user/maps us-forecast
```
This command creates a new directory called ```maps``` in your local working directory
and mounts it to the container. Then it runs the forecast script inside the container. This allows the map ```.png``` files to be
saved on your machine. 