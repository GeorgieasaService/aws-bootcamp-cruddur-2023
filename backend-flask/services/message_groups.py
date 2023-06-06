from datetime import datetime, timedelta, timezone

from lib.ddb import Ddb
from lib.db import db # need the db to find the handle from the uuid

class MessageGroups:
  def run(cognito_user_id):
    print(f"printing the cognito_user_id: {cognito_user_id}")
    model = {
      'errors': None,
      'data': None
    }
    
    print('-----message_groups.py Testing-----')
    sql = db.template('users','uuid_from_cognito_user_id') # this block of code performs a permissions check
    my_user_uuid = db.query_value(sql,{
      'cognito_user_id': cognito_user_id
    })
  
    print(f"UUID: {my_user_uuid}")
    print('cognito_user_id in message_groups.py----', cognito_user_id)

    ddb = Ddb.client()
    data = Ddb.list_message_groups(ddb, my_user_uuid)
    for item in data:
      print("list_message_groups: ",data)

    model['data'] = data
    return model