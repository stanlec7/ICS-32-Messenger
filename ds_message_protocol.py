import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['type','token','message'])

def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object

    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    '''
    message=[]
    #print("json_msg in protocol", json_msg)
    json_obj = json.loads(json_msg)

    try:
        #print("in")
        json_obj = json.loads(json_msg)
        #print("uh")
        #print("Here:",json_obj['type'])
        Type = json_obj['response']['type']
        try:
            message.append(json_obj['response']['message'])
        except:
            pass
        try:
            token=json_obj['response']['token']
            #message=json_obj['response']['messages']
            
        except KeyError:
            token=""
        try:
            dmList = json_obj['response']['messages']
            for x in range(len(dmList)):
                #s1=json_obj['response']['messages'][x]['message'] +' '+ json_obj['response']['messages'][x]['from'] +' '+ json_obj['response']['messages'][x]['timestamp']
                #for key in dmList[x]:
                    #print(dmList[x][key])
                
                timestamp = json_obj['response']['messages'][x]['timestamp']
                user = json_obj['response']['messages'][x]['from']
                msg = json_obj['response']['messages'][x]['message']

                message.append((timestamp,user,msg))
                #dmList[x]=dm
        except KeyError:
            message="hi"
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(Type,token, message)
'''
string="{\"response\": {\"type\": \"ok\", \"messages\": [{\"message\":\"Hello User 1!\", \"from\":\"markb\", \"timestamp\":\"1603167689.3928561\"},{\"message\":\"Bzzzzz\", \"from\":\"thebeemoviescript\", \"timestamp\":\"1603167689.3928561\"}]}}"
print(string)
s2="{\"response\": {\"type\": \"ok\", \"message\": \"Direct message sent\"}}"
print(extract_json(string))

'''
