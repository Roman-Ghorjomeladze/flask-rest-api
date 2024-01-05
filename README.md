# Description
This is a demo api developed with Flask
# How to guide

## To build docker image run:
```bash
  docker build -t [YOUR_DOCKER_USER]/[APP_NAME] . 
```

## To run flask app in watch mode inside docker container: 
```bash
  # Run app in background (you can access logs from docker desktop app)
  docker run -dp 5000:5000 -w /app -v "$(pwd):/app" [YOUR_DOCKER_USER]/[APP_NAME] 
  # Run app in foreground (you can view logs in terminal)
  docker run -p 5000:5000 -w /app -v "$(pwd):/app" [YOUR_DOCKER_USER]/[APP_NAME]
```

## Run flask app without watch mode:
```bash
  docker run -dp 5000:5000 [YOUR_DOCKER_USER]/[APP_NAME] 
```


### Keywords
#Rest #Python #Flask #CRUD #API