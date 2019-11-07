echo "==========================="
echo "Stagging Server"
echo "==========================="
export FLASK_ENV=development
export FLASK_APP=app.py
export APP_SETTINGS="config.StaggingConfig"
export SECRET_KEY=kamseupai2019onfire17081945
export HOST_MODE=development 
export GOOGLE_OAUTH_CLIENT_ID=1010640175796-vnp220hj8ceepbniguvrvifju99bi398.apps.googleusercontent.com
export GOOGLE_OAUTH_CLIENT_SECRET=5VBRMSPo32XiuL4N5h481zqJ
export OAUTHLIB_RELAX_TOKEN_SCOPE=true
export OAUTHLIB_INSECURE_TRANSPORT=true

export db_type=postgresql
export username=admin
export password=admin
export host=localhost
export port=5432
export database=kamseupai

. env/bin/activate
echo "source of env was activated"
flask run -p 5001