<img src="https://github.com/thomktz/betterave/assets/82711723/4649d8fd-837b-4be4-93c5-6212d36d7d88" width="200" height="100" alt="betterave-logo">  


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


## Features

There are 4 types of user profiles in the software, each with different features and restrictions:

- **Student Profile:**
  - View schedule and grades
  - Manage course registrations and check assignments
  - Access the class roster
  - Subscribe to news from student associations at the school

- **Association Profile (managed by a student):**
  - Create events
  - Send notifications to subscribed students

- **Teacher Profile:**
  - View schedule
  - Enter grades
  - Assign homework to students

- **Administrator Profile:**
  - Add or remove users

Here you can find demonstration videos according to the type of users:

[Student demo](https://www.youtube.com/watch?v=zZC0X2hOou0)

[Association demo](https://www.youtube.com/watch?v=YLPqCE9lRXs&feature=youtu.be)

## Database Stucture

![Diagramme de la base de données](https://github.com/thomktz/betterave/assets/82711723/28393118-e898-405b-9c2a-8fb463c8a8af)

## API Structure 

RESTful 


## Code standards 

- **Using Pre-Commit**  
  If you wish to integrate Pre-Commit into your workflow, simply follow these steps:
  - Install Pre-Commit in your Python environment using the following command:
     ```pip install pre-commit```
  - Run the following command to set up Pre-Commit in your repository:
     ```pre-commit install```
  - If you want to manually run hooks on files you've modified and staged, use the command:
      ```pre-commit run```
  - To run hooks across the entire codebase, including all files, use the command:
      ```pre-commit run --all-files```

- **Code review and Pull requests**  
  We encourage collaboration through the use of pull requests (PRs) for proposing changes to the codebase:
  - **Fork the Repo:** Fork the repository to your GitHub account.
  - **Create a Branch:** Start a new branch for your changes.
  - **Make Changes:** Implement your code changes in the branch.
  - **Commit & Push:** Commit changes and push to your fork.
  - **Open a Pull Request:** Propose changes through a pull request.
  - **Code Review:** Team members review and provide feedback.
  - **Address Feedback:** Make necessary changes based on feedback.
  - **Merge:** Once approved, changes are merged.

- **Testing**  
  To test the code, run `pytest` in the source directory. This will exercise the unit tests (using [pytest](https://docs.pytest.org/)) and generate a coverage report.

## Deployment

Docker
Serveur
DNS

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

- Notifications functionnality to be finished








