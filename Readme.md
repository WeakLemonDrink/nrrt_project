# Node Relationship Ranking Table web application

## Requirements
The web application is developed with [Python 3.7.9](https://www.python.org/downloads/release/python-379/) using [Django 3.1.2](https://docs.djangoproject.com/en/3.1/releases/3.1.2/).

Full requirements are provided in [requirements.txt](requirements.txt).

## The development environment
The development environment should be set up using a virtual environment created using [virtualenv](https://virtualenv.pypa.io/en/stable/) and [pip](https://pypi.org/project/pip/). Once an environment has been set up, the [dev_setup_env.sh](./scripts/dev_setup_env.sh) shell script can be used to load the environment to develop the project. The following environment variables are required:

* SECRET_KEY

The values for this variable is provided outside of this repository for security and should be copied to a `.env` file in the project root.
