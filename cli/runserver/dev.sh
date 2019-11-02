
echo "==========================="
echo "Development Server"
echo "==========================="
export FLASK_ENV=development
export FLASK_APP=app.py
export APP_SETTINGS="config.DevelopmentConfig"
export HOST_MODE=development 
export SECRET_KEY=kamseupai2019onfire17081945
. env/bin/activate
echo "source of env was activated"
exec flask run 