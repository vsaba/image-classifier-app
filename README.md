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

#### docker compose up --build

or run the docker-desktop application, navigate to the container field and run the container: image-classifier-app