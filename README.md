*Projet Infrastructures et systèmes logiciels*

## **Better**ave: Pamplemousse 2.0
- Calendar management
- Class groupchats
- Homework
- Association notification and events
- Trombinoscope
  
<img width="1728" alt="image" src="https://github.com/thomktz/betterave/assets/60552083/ce64adce-a47b-4d20-8f25-34d51f73d60b">




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

To shut down the containers:
```bash
docker compose down
```

And to see the logs, 
```bash
docker compose logs
```