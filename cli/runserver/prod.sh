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



echo "==========================="
echo "Production Server"
echo "==========================="
export FLASK_ENV=production
export APP_SETTINGS=config.ProductionConfig
export HOST_MODE=production 
export SECRET_KEY=kamseupai2019onfire17081945
export GOOGLE_OAUTH_CLIENT_ID=1010640175796-vnp220hj8ceepbniguvrvifju99bi398.apps.googleusercontent.com
export GOOGLE_OAUTH_CLIENT_SECRET=5VBRMSPo32XiuL4N5h481zqJ
export OAUTHLIB_RELAX_TOKEN_SCOPE=true
export OAUTHLIB_INSECURE_TRANSPORT=true

export db_type=postgresql
export username=kamseupai
export password=kamseupai
export host=localhost
export port=5432
export database=kamseupai

# GUNICORN SERVER
exec gunicorn app:app -b 0.0.0.0:5000 \
 --reload \
 --workers 2 \
 --log-level=false \
 --access-logfile history/logs \
 --log-file=-

