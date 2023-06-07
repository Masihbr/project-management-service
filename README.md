# project-management-service
Project management service as a coding challenge.

# Run
```py
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
// if ran to error use
while read requirement; do pip install $requirement || break; done < requirements.txt
// endif
python manage.py migrate
python manage.py runserver
```

# Docker
Use below command for dockerized view
```py
docker-compose --env-file docker-compose.env up --build
```