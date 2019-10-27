sudo rm apps/data.sqlite
sudo rm -rf apps/migrations
python manage.py db init 
python manage.py db migrate
python manage.py db upgrade
