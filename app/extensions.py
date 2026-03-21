from flask import Flask, render_template,redirect,flash,url_for,abort,request,g,session,jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,TextAreaField,BooleanField,SelectField
from wtforms.validators import InputRequired,Length,EqualTo
import os
import requests
import datetime
from datetime import timedelta
import json
from helpers import Json2Object,get_data,Object2Json,convert_json
from app.mailing import Send_Email
from random import randrange,sample
import numpy
from itsdangerous import SignatureExpired,BadTimeSignature,URLSafeTimedSerializer


db = SQLAlchemy()
bcrypt = Bcrypt()
#-------------Admin info-----------
ADMIN_FIRST_NAME='ADMIN_FIRST_NAME'
ADMIN_LAST_NAME='ADMIN_LAST_NAME'
ADMIN_EMAIL='ADMIN_EMAIL'
ADMIN_PASSWORD='ADMIN_PASSWORD'
EMAIL_RESET='EMAIL_RESET'
#---------------end-----------------

RECIPE_ITEM = "recipe_item"
CURR_USER_KEY = "curr_user_key"

API_URL_BASE ="https://tasty.p.rapidapi.com"
headers = {
	"X-RapidAPI-Key": os.getenv('API_KEY',None),
	"X-RapidAPI-Host": "tasty.p.rapidapi.com"
}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')


#for local testing google oauth in http
# export OAUTHLIB_INSECURE_TRANSPORT=1
google_client_config = {
    "web": {
        "client_id": os.getenv('GOOGLE_CLIENT_ID',None),
        "project_id": os.getenv('GOOGLE_PROJECT_ID',None),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET',None),
        "redirect_uris":[f"{os.getenv('GOOGLE_REDIRECT_URI_BASE',None)}/auth/google/callback"],
    }
}
