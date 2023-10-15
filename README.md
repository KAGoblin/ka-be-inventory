# ka-starter-api
Template Repository with defined Django-Oscar configs required for academic research purpose on XYZ Corp

## Setup
### Environment Setup (tested on Ubuntu 22.04)
- Install Python 3
```
sudo apt install python3
```
- Install PostgreSQL
```
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service
```
- Install pip
```
sudo apt install python3-pip
```
- Install pyenv
  - https://itslinuxfoss.com/install-use-pyenv-ubuntu/
  - install & use Python 3.10.2
- Install pipenv
```
python -m pip install pipenv
```

### Development Setup (tested on Ubuntu 22.04)
- Run make install (please see Makefile for detailed instruction)
```
make install
```
- create .env file on the root project folder, here's the list of environment variables
```
DEBUG=True
SECRET_KEY=abcde
DB_CRED_USERNAME=username
DB_CRED_HOST=
DB_CRED_NAME=kastarter
DB_CRED_PASSWORD=
```

### Run
- Command
```
pipenv run python manage.py runserver
```
- Your app should now be running on localhost:8000.

## What Should be Replaced for Creating New Service

- Update its **.env** file [Secret Key Generator](https://www.miniwebtool.com/django-secret-key-generator/)
- Replace the name of its **main folder**
- Replace the default port in **manage.py** file, avoid using port that is already in use by other microservices
- Update the default port and other info in **README.md** file
- Replace name of _PROJECT_APPS_ **settings.py** file
