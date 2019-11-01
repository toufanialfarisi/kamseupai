export FLASK_ENV=development
export FLASK_APP=app.py
export APP_SETTINGS="config.StaggingConfig"
export HOST_MODE=development 
export GOOGLE_OAUTH_CLIENT_ID=1010640175796-vnp220hj8ceepbniguvrvifju99bi398.apps.googleusercontent.com
export GOOGLE_OAUTH_CLIENT_SECRET=5VBRMSPo32XiuL4N5h481zqJ
export OAUTHLIB_RELAX_TOKEN_SCOPE=true
export OAUTHLIB_INSECURE_TRANSPORT=true

. env/bin/activate
echo "==========================="
echo "source of env was activated"
echo "==========================="
flask run  