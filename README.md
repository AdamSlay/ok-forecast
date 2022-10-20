# Oklahoma Hourly Forecast Map
This is a simple Forecast Map using weather data from Weather.gov to display the hourly forecast.
My primary goals with this project were to utilize asynchronous programing and Docker. 

## Running the program
To run the program, clone the repo then execute the following command while in the project directory:
```bash
docker build -t ok-forecast .
```
then:
```bash
docker run ok-forecast
```