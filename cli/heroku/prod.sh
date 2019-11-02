heroku config:set APP_SETTINGS=config.ProductionConfig
heroku config:set FLASK_ENV=production
heroku config:set HOST_MODE=production
heroku config:set SECRET_KEY=kamseupai2019onfire17081945
heroku config:set GOOGLE_OAUTH_CLIENT_ID=1010640175796-vnp220hj8ceepbniguvrvifju99bi398.apps.googleusercontent.com
heroku config:set GOOGLE_OAUTH_CLIENT_SECRET=5VBRMSPo32XiuL4N5h481zqJ
heroku config:set OAUTHLIB_RELAX_TOKEN_SCOPE=true
heroku config:set OAUTHLIB_INSECURE_TRANSPORT=true

heroku config:set db_type=postgresql
heroku config:set username=rqjlcbouwdptml
heroku config:set password=140d296ff6a2103213affa9eaeaa8b3f2d24cb15c1b9a321ce77277db35bca55
heroku config:set host=ec2-54-197-238-238.compute-1.amazonaws.com
heroku config:set port=5432
heroku config:set database=da3kp68t3m2lui