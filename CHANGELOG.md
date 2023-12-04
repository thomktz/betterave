# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.2.0] - 2023-12-01
### Added
- New Student controls page
- Delete UCGs when updating student level
- Added delete event route
- New Asso Controls page

### Changed
- Switched to HH:MM format for time inputs


## [3.1.0] - 2023-11-11
### Added
- Register page
- user_post_model
- Export toast from apiConfig
- .env.local creation script

### Changed
- Visual overhaul to the EditClasses page
- Redo readme

# [3.0.1] - 2023-11-10
### Added
- Special error handling on check-auth failure -> Don't show toast
- Always logout user when loading login page

# [3.0.0] - 2023-11-09
Major API changes, from flask to flask-restx
### Added
- RestX Models, namespaces, routes for all SQLAlchemy models
- Decorators for authentication and authorization
- User.is_student, User.is_teacher, User.is_admin, properties
- Website logo
- apiConfig and apiClient to handle api calls

### Changed
- Major frontend changes to accomodate new api

### Removed
- Flask routes

# [2.1.0] - 2023-11-08
### Added
- Docker support
- Dockerfiles and docker-compose.yml
- .env files

### Changed
- vue.config.js to allow for docker build

### Fixed
- missing pandas dependency


## [2.0.0] - 2023-11-06

### Added - backend

- New ClassGroup model to handle groups within a class (TD, TP, Cours).
- Associated operations, routes and tests.
- New UserClassGroup model to handle (user, class, main_group, secondary_group) relationships
- Associated operations, routes and tests.
- @with_instance decorator to make operations more flexible
- display_classes script
- CHANGELOG.md

### Added - frontend
- Control pages - AdminControls, AssoControls and TeacherControls
- EditClasses view and associated components

### Changed
- Full revamp of init_db, tests, routes, opperations and model relationships.

### Removed
- "Authorized" mechanics for teachers/classes