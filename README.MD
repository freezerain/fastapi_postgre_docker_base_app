adress: http://127.0.0.1:8008/
build: $ docker-compose up -d --build
clean: $ docker-compose down --volumes
test: $ docker-compose exec web pytest .
postgre test: $ docker-compose exec db psql --username=entropy_testuser --dbname=entropy_db
    # # \l
    # # \c entropy_db
    # # \dt
    # # \q
DEV TODO: 
-Doc  http://127.0.0.1:8008/docs

TODO: 
-Gunicorn
-Traefik/Nginx router
-LetsEncrypt certificated and domain name
