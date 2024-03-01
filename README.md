<img src="https://github.com/thomktz/betterave/assets/82711723/4649d8fd-837b-4be4-93c5-6212d36d7d88" width="200" height="100" alt="betterave-logo">

_ENSAE année 2023-2024 : Projet Infrastructures et systèmes logiciels_

**Link to the website** : [betterave.kientz.net](https://betterave.kientz.net)
Link to the API : [api.betterave.kientz.net](https://api.betterave.kientz.net)

## Table of Contents

- [Introduction](#betterave-pamplemousse-20)
- [Features](#features)
- [Repository Organization](#repository-organization)
- [Database Structure](#database-structure)
- [API Structure](#api-structure)
- [Frontend](#frontend)
- [Code Standards](#code-standards)
- [Deployment](#deployment)
- [Setup for Development](#setup-for-development)
- [Difficulties and Areas for Improvement](#difficulties-and-areas-for-improvement)

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

**Link to the website** : [betterave.kientz.net](https://betterave.kientz.net)

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
  - All teacher and association features

**Here you can find demonstration videos according to the type of users**:

[Student demo](https://www.youtube.com/watch?v=zZC0X2hOou0)

[Association demo](https://www.youtube.com/watch?v=YLPqCE9lRXs&feature=youtu.be)

[Admin and teacher demo](https://www.youtube.com/watch?v=L9cUxl0pSjQ)

Login is handled using flask-login, and the password is hashed using bcrypt, before being stored in the database.

## Repository Organization

The repository is structured into three main directories:

- `backend`: Manages the definition of database structures, API development, and unit tests.
- `frontend`: Encompasses all aspects related to the user interface, including images, web scripts, and other frontend-specific files.
- `scripts`: Dedicated to scripts used for tasks such as generating the virtual environment or other related functionalities.

This organization ensures a clear separation of concerns between the backend and frontend, providing an organized space for frontend components, visual elements, and scripts.

## Database Stucture

While coding the data structure, we incrementally added tables to fit new features. We first started off with only Students and Classes, and then realized the need for Lessons, Groups, etc.

- User Table: Stores user information for the application (type of the user, name, username, email...).
- Grade Table: Stores student grades (student_id, class_id, grade...)
- Class Table: Stores information about a class (teacher,...). Each class has several lessons, groups, and homework.
- Lesson Table: Stores information about the different lessons of a class (date, place...).
- Homework Table: Stores information about homework of a specific class (content, due date...).
- Class_Group Table: Stores information about a specific group of a class (attending students, class_id ...)
- User_Class_Group Table: Stores the relationship between a student and the class that the student subscribed to.
- Group_Enrollment Table: Stores the relationship between a student and the specific class group that the student subscribed to.
- Homework Table: Stores information about a homework (corresponding class, due date, due time...).
- Event Table: Stores information about an event (association, date...).
- Event_Attendance Table: Stores the attending relationship between a student and an event.

The data for classes was scraped from the ENSAE website, and the data for the lessons calendar was scraped from Pamplemousse, using BeautifulSoup.

![Relationship diagram of de database](https://github.com/thomktz/betterave/assets/82711723/28393118-e898-405b-9c2a-8fb463c8a8af)

## API Structure

This application is built using Flask-RESTx (branch of Flask-RESTful), a Flask extension designed to simplify the development of RESTful APIs. Flask-RESTful streamlines the process of creating API endpoints, managing resources, and incorporating RESTful features seamlessly.

The organized structure of the API allows us to easily create an API page, which provides a clear overview of the API endpoints and their respective functionalities. Link to the API : [api.betterave.kientz.net](https://api.betterave.kientz.net)

### API Scripts Location

All scripts related to the API are centralized in the `backend/app/api` directory. Within this directory, you'll find various subfolders:

- `auth`
- `class_groups`
- `classes`
- `events`
- `lessons`
- `user_class_groups`
- `users`

### Key Files

- `routes.py`: This file contains the route definitions for different API endpoints.
- `models.py`: Here, you'll find the data models used by the application.

This organized structure enhances the clarity and maintainability of the API implementation.

## Frontend

The frontend of this application is built using [Vue.js](https://vuejs.org/), a JavaScript framework. It provides a user-friendly interface for interacting with the backend services.
Within this directory, you'll find two main subfolders:

- `public` (houses logos, photos displayed on the app)
- `src` (houses the Vue scripts, font files, and style configurations that contribute to the frontend functionality and appearance...)

We used **vuetify** for tables and form elements, but coded many components ourselves, such as the grade table, the groupchats, the next classes, etc.

## Code standards

- **Package managing**
  Environments were managed using Poetry in Python and Npm in Vue.js.

- **Using Pre-Commit hooks**  
  Pre-commit allows you to run scripts ('hooks') before each commit to your repository. The ones we used are **black** (python - code formatter), **flake8** (python - linter) and **prettier** (js/vue - code formatter).

  To run them, you should install the hooks using `pre-commit install`, and then `pre-commit run`

- **Code review and Pull requests**  
  We encourage collaboration through the use of pull requests (PRs) for proposing changes to the codebase:

  - **Create a Branch:** Start a new branch for your changes.
  - **Make Changes:** Implement your code changes in the branch.
  - **Commit & Push:** Commit changes and push to your fork.
  - **Open a Pull Request:** Propose changes through a pull request.
  - **Code Review:** Team members review and provide feedback.
  - **Address Feedback:** Make necessary changes based on feedback.
  - **Merge:** Once approved, changes are merged.

- **Testing**  
  To test the code, execute `pytest` in the source directory. This command will run the unit tests (using pytest) and generate a coverage report. Our tests cover mostly the database operations, which is critical when developing an API, since routes are just shallow interfaces to the operations. Our test suite contains **68 tests**.

- **ChangeLog**

  We started a [CHANGELOG.md](https://github.com/thomktz/betterave/blob/main/CHANGELOG.md) to keep track of versions and the features added by each PR

## Deployment

### Docker

The code is containerized using Docker. Both frontend and backend have their Dockerfile, and a `docker-compose.yml` in the root folder is used to orchestrate them, and the database/volumes. More information on how to setup the app for development can be found in the Setup for Development section.

The compose file also allows us to use a specific address for the frontend and backend within a docker network, which is useful for the reverse proxy.

### Server

To host our app, we used a free-tier EC2 instance from Amazon Web Services. The instance is running Ubuntu 22.04, and is accessible through SSH. We installed Docker and then cloned the repository.

### DNS

Luckily enough, we already had a domain name for us to use - or rather to create a subdomain from. On the server, we set up a reverse proxy to redirect requests to the right port.

- betterave.kientz.net redirects to port 8080 (frontend)
- api.betterave.kientz.net redirects to port 5000 (backend)

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

To scrap ENSAE website, run :

```bash
docker exec -it betterave-backend-1 python -m scripts.scraping
```

To initialize the database, run :

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
