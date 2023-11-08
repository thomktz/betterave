# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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