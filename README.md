_Projet Infrastructures et systèmes logiciels_

## **Better**ave: Pamplemousse 2.0

- Calendar
- Class groupchats
- Homework
- Grades
- Association events
- Trombinoscope
- Class scraping from Pamplemousse and the ENSAE website
- Light/dark theme

<img width="1200" alt="image" src="https://github.com/thomktz/betterave/assets/60552083/353cdd6b-93d0-4354-9c99-0f1bbd496da7">
<img width="1200" alt="image" src="https://github.com/thomktz/betterave/assets/60552083/fc2ca296-6561-4ae6-9f07-64ac2f41b01e">

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
