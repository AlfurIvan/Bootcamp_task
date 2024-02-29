There is a project created for Boot Camp 2024.

SETUP STEPS:


    sudo docker-compose up -d --build
    sudo docker-compose exec api python manage.py loaddata data.json
Optional:

    sudo docker-compose exec api python manage.py createsuperuser
    sudo docker-compose exec api python manage.py test
    sudo docker-compose exec api flake8 --ignore=E501,F401


 - According to task:
   -  Application is containerized.
   -  There are 3 entities in PostgreSQL database: Profession, Skill, Topic.
   - CRUD operations for each entity 
     - http://0.0.0.0:8000/entity_name/ to create(and list)
     - http://0.0.0.0:8000/entity_name/{uuid}/ to retrieve, update and delete

    
- Retrieve all professions and their associated skills and topics. 
  - http://0.0.0.0:8000/professions/ 
- Retrieve all skills and their associated topics.
  - http://0.0.0.0:8000/skills/


 - Testing:


    sudo docker-compose exec api python manage.py test
