export FLASK_ENV=development
export FLASK_APP=app.py
export APP_SETTINGS="config.StaggingConfig"
export HOST_MODE=development 
. env/bin/activate
echo "==========================="
echo "source of env was activated"
echo "==========================="
exec flask run  