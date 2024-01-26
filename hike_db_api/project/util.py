def convert_user_json_to_dict(jsonObject):
    
    userDict = {
    "password":jsonObject.get('password',None),
    "first_name":jsonObject.get('first_name',None),
    "last_name":jsonObject.get('last_name',None),
    "email":jsonObject.get('email',None)
    }

    return userDict
