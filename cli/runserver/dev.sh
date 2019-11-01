export FLASK_ENV=development
export FLASK_APP=app.py
export APP_SETTINGS="config.DevelopmentConfig"
export HOST_MODE=development 
. env/bin/activate
echo "==========================="
echo "source of env was activated"
echo "==========================="
python app.py