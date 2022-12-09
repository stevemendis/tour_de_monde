from cerberus import Validator
import re
from datetime import datetime

def check_password(field, value, error):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,16}$"
    # compiling regex
    match_re = re.compile(reg)
    # searching regex
    res = re.search(match_re, value)
    # validating conditions
    if not res:
        error(field, "Invalid Password")

to_date = lambda s: datetime.strptime(s, '%Y-%m-%d')

user_signup = {
            'first_name': {'required': True, 'type': 'string'},
            'last_name' : {'required': True, 'type': 'string'},
            'phone_number': {'required': True,
                                'type': 'string', 
                                'minlength': 10, 
                                'maxlength': 10, 
                                'regex': '^[0-9]*$'},
            'date_of_birth': {'required': True, 'type': 'datetime', 'coerce': to_date},
            'gender': {'required': True, 'type': 'string'},
            'username': {'required': True, 'type': 'string'},
            'email': {'required': True,
                        'type': 'string', 
                        'minlength': 8, 
                        'maxlength': 255, 
                        'required': True,
                        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'},
            'password': {'required': True, 'type': 'string', 'validator': check_password}}

user_login = {
                'username': {'required': True, 'type': 'string'},
                'password': {'required': True, 'type': 'string', 'validator': check_password}
                }