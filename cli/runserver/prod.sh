# DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
# echo ${DIR}
# cd ../../${DIR}

. env/bin/activate
echo "=========================="
echo "ENVIRONMENT WAS ACTIVATED"
echo "=========================="

pip install -r requirements.txt
echo "=========================="
echo "PIP WAS INSTALLED"
echo "=========================="



export FLASK_ENV=production
export APP_SETTINGS=config.ProductionConfig
export HOST_MODE=production 
export SECRET_KEY=kamseupai2019onfire17081945

# GUNICORN SERVER
exec gunicorn app:app -b 0.0.0.0:5000 \
 --reload \
 --workers 2 \
 --log-level=false \
 --access-logfile history/logs \
 --log-file=-

