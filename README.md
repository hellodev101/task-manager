# Introduction

This project is designed to help users manage their tasks efficiently by providing a user-friendly interface to organize, to keep track of tasks during the sprint, a set period in which specific tasks are completed, by team members.

## Table of Contents

- [Installation](#installation)

## Installation

### Prerequisites

Pyenv is a powerful tool that allows developers to easily manage multiple versions of Python on their systems. It simplifies the process of switching between different Python versions, which is particularly useful for projects that require specific Python environments.

    pyenv -(https://github.com/pyenv/pyenv-installer)

1. We are going to be using Python version 3.11 in the project, so let's get that installed with the following command:

```bash
pyenv install 3.11
```

2. Install poetry. If you want to know more about what poetry is, please visit this link (https://pypi.org/project/poetry/).

```bash
pip install poetry
```

3. Install the dependencies for the project:

```bash
poetry install
```

4. Activate poetry virtualenv:

```bash
poetry shell
```

5. Start docker container by running the following command:

```bash
docker-compose up -d
```

6. Create migration files:

```bash
python manage.py makemigrations
```

7. Appy the migations to the database:

```bash
python manage.py migrate
```

8. Now you should be able to run the development server:

```bash
python manage.py runserver
```
