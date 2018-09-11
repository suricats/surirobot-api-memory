# Surirobot Memory API

API made with Django used to retrieve some informations stored by the surirobot.
The informations include data like sensors, identifications, various logs, and pictures.
Currently made to be a POC. The function of this repository may change in the future.

## Requirements

* Python3 
* Virtualenvwrapper ```pip install virtualenvwrapper```
* If you have some trouble with the command ```workon``` see : https://stackoverflow.com/questions/29900090/virtualenv-workon-doesnt-work

## Installation

### Using Docker

```shell
docker build . -t api-memory
docker run --env-file .env -p 8000:8000 api-memory
```

### From source

* Clone repository 
* Create virtualenv
```shell
mkvirtualenv api-memory && workon api-memory
```

* Install dependencies
```shell
pip install -r requirements.txt
```

## Configure the environment file
* Configure .env
```shell
cp .env.example .env
```
If you want to use the default environment
- Fill only the ```REMOTE_DATA_LOGIN```  and ```REMOTE_DATA_PASSWD``` fields
- Run the command : ```tools/get-env```

* Run the dev server
```shell
cd api
python manage.py runserver
```

## Docs
