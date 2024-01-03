### Image classifier application

This is a simple web application that implements allows a user to randomly choose an
image of a handwritten written number and predict the number on the image using a classifier model.
<br>
<br>
The web application can be containerized using the docker file in the repository.
Simply clone the repository in your local system, ensure you have docker installed on your system,
and in the cloned directory run the following command:

#### docker compose up --build

This will create a docker image and run the image. Every subsequent time you wish to run the application,
simply run the following command:

#### docker compose up

or run the docker-desktop application, navigate to the container field and run the container: image-classifier-app

#### IMPORTANT:

Before running the container please ensure the port 5432 is not in use. If there is an error with running the
docker container, usually the following command will solve the problem:

#### sudo service postgresql stop

Should you encounter any other problems with running the container, feel free to contact me.