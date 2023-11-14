# file-fortress

A file hosting service

## Requirements

* [Docker Compose](https://docs.docker.com/compose/install/)

## Installation/Setup

### Database

The MariaDB container requires some environment variables to be set.
When using Docker Compose, the file `mariadb/.env` should be created with the following values filled in:

```
MARIADB_ROOT_PASSWORD=<ROOT PASSWORD>
MARIADB_USER=<USER ACCOUNT>
MARIADB_PASSWORD=<USER PASSSWORD>
```

Note the default database can be changed from `filefort` via the `MARIADB_DATABASE` environment variable in `docker-compose.yml`.

## Usage

## Contributors

* [JP Appel](https://github.com/jpappel)
* [Owen Halliday](https://github.com/drekdrek)
* [David Marrero](https://github.com/badlydrawnface)
