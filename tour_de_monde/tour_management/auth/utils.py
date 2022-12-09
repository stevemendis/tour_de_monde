from tour_management import login_manager
from tour_management.models import User
from tour_management.models import Admin
from base64 import b64encode
from base64 import b64decode
from flask import redirect, url_for, render_template, current_app
import json
import os
import re
import requests



@login_manager.user_loader
def load_user(user_id):
    x = Admin.query.get(user_id)
    if x == None:
        x = User.query.get(user_id)
    return x