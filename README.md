<img src="https://github.com/thomktz/betterave/assets/82711723/4649d8fd-837b-4be4-93c5-6212d36d7d88" width="100" height="100" alt="betterave-logo">  


_ENSAE année 2023-2024 : Projet Infrastructures et systèmes logiciels_ 

## **Better**ave: Pamplemousse 2.0

Betterave is a school management software designed for students and professors at ENSAE. It incorporates the main features of the existing software 'Pamplemousse' but also introduces new functionalities:
- Class schedule  
- Grades
- Photochart 
- **Class groupchats (new)**
- **Homework (new)**
- **Association events (new)**
- **Light/dark theme (new)**



<img width="1200" alt="image" src="https://github.com/thomktz/betterave/assets/60552083/353cdd6b-93d0-4354-9c99-0f1bbd496da7">
<img width="1200" alt="image" src="https://github.com/thomktz/betterave/assets/60552083/fc2ca296-6561-4ae6-9f07-64ac2f41b01e">


## Demonstration videos

[Student demo](https://www.youtube.com/watch?v=zZC0X2hOou0)
[Association demo](https://www.youtube.com/watch?v=YLPqCE9lRXs&feature=youtu.be)


## Database Stucture

## API

## Setup for development

- Install [Docker](https://docs.docker.com/get-docker/).
- Clone the repository.
- Navigate to the root of the repository. (`cd betterave`)
- For local development, you must generate the .env.local by running the script:

```bash
./scripts/generate_local_env.sh
```

- For server deployment, no need to generate the .env.local since the existing .env file will be used.
- Run the following command to start the containers:

```bash
docker compose up --build
```

Or, if you want to run the containers in the background:

```bash
docker compose up --build -d
```

Scraping ENSAE website
```bash
docker exec -it betterave-backend-1 python -m scripts.scraping
```

Initiate the database
```bash
docker exec -it betterave-backend-1 python -m scripts.init_db
```

To shut down the containers:

```bash
docker compose down
```

And to see the logs,

```bash
docker compose logs
```
## Difficulties and Areas for Improvement
