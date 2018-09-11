# Surirobot Memory API

API made with Django used to retrieve some informations stored by the surirobot.
The informations include data like sensors, identifications, various logs, and pictures.
Currently made to be a POC. The function of this repository may change in the future.

## Requirements

* Python3 
* Virtualenvwrapper ```pip install virtualenvwrapper```
* If you have some trouble with the command ```workon``` see : https://stackoverflow.com/questions/29900090/virtualenv-workon-doesnt-work

## Installation 

* Clone repository 
* Create virtualenv
```shell
mkvirtualenv api-memory && workon api-memory
```

* Install dependencies
```shell
pip install -r requirements.txt
```

* Configure .env with database informations
```shell
cd api
cp .env.example .env
```

* Run the server
```shell
cd api
python manage.py runserver
```

## Docs
