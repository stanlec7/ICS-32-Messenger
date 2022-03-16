import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['type','token','message'])

def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object
    '''
    message=[]
    json_obj = json.loads(json_msg)
    try:
        json_obj = json.loads(json_msg)
        Type = json_obj['response']['type']
        try:
            message.append(json_obj['response']['message'])
        except:
            pass
        try:
            token=json_obj['response']['token'] 
        except KeyError:
            token=""
        try:
            dmList = json_obj['response']['messages']
            for x in range(len(dmList)):
                timestamp = json_obj['response']['messages'][x]['timestamp']
                user = json_obj['response']['messages'][x]['from']
                msg = json_obj['response']['messages'][x]['message']
                message.append((timestamp,user,msg))
        except KeyError:
            message="hi"
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    return DataTuple(Type,token, message)

