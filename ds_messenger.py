import socket
import ds_message_protocol
import time
from Profile import Post, Profile

class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None
        self.msg_list=[]

    def set_message(self, message, recipient):
        self.message=message
        self.recipient=recipient
        self.timestamp=str(time.time())
        print('done setting')
        #print(self.msg_list)
        #Dict = {'Name': 'Geeks', 1: [1, 2, 3, 4]}
        #msg_dict= {"message": self.message, "from": self.recipient, "timestamp":self.timestamp}
        #print("before",self.msg_list)
        #print("inside set message")
        #self.msg_list.append(msg_dict)
        #print("after",self.msg_list)


class DirectMessenger(DirectMessage):
    server="168.235.86.101"
    username="blahblahblah"
    password="hello"
    
    def __init__(self, dsuserver=None, username=None, password=None):
        super().__init__()
        #self.token = None
        if (dsuserver!=None):
            self.server=dsuserver
        if (username!=None):
            self.username=username
        if (password!=None):
            self.password=password
        self.last_time=None
        self.pf=Profile(self.server,self.username,self.password)
        
        self.port=3021
        self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server, self.port))
        join_msg=self.join()
        self.client.sendall(join_msg.encode('utf-8'))
        rev_msg=self.client.recv(4096)
        #print("join receive msg", rev_msg)
        DataTuple=ds_message_protocol.extract_json(rev_msg.decode('utf-8'))
        if (DataTuple.type!="error"):
            self.token=DataTuple.token
        '''
        self.recipient = None
        self.message = None
        self.timestamp = None
        '''

    def join(self)->str:
        result="{\"join\": {\"username\": \""+self.username+"\",\"password\": \""+self.password+"\",\"token\":\"""\"}}"
        return result

    def post(self)->str:
        print('in')
        #result="{\"token\":\""+self.token+"\", \"directmessage\": {\"entry\": \""+self.message+"\",\"recipient\":\""+self.recipient+"\", \"timestamp\": \"1603167689.3928561\"}}"
        result="{\"token\":\""+self.token+"\", \"directmessage\": {\"entry\": \""+self.message+"\",\"recipient\":\""+self.recipient+"\", \"timestamp\": \""+self.timestamp+"\"}}"
        return result

    #def connect(
    	
    def send(self, message:str, recipient:str) -> bool:
        # returns true if message successfully sent, false if send failed.
        super().set_message(message,recipient)
        validity=True
        postValid=True
        if (self.message!=""):
            post_msg=self.post()
            #print("post_msg",post_msg)
            self.client.sendall(post_msg.encode('utf-8'))
            rev_msg=self.client.recv(4096)
            DataTuple=ds_message_protocol.extract_json(rev_msg.decode('utf-8'))
            if (DataTuple.type=="error"):
                validity=False
        else:
            postValid=False
        return validity and postValid
                
        #return (validity and joinValid and postValid)

    def new(self)->str:
        result="{\"token\":\""+self.token+"\", \"directmessage\": \"new\"}"
        return result
		
    def retrieve_new(self) -> list:
        # returns a list of DirectMessage objects containing all new messages
        new_msg=self.new()
        self.client.sendall(new_msg.encode('utf-8'))
        rev_msg=self.client.recv(4096)
        DataTuple=ds_message_protocol.extract_json(rev_msg.decode('utf-8'))
        print('retrieve_new datatuple:', DataTuple)
        msgList=DataTuple.message
        print('msgList in retrieve_new:', msgList)
        index=0
        returnList=[]
        while(index<len(msgList)):
            returnList.append(msgList[index])
            index+=3
        #print(returnList)
        return returnList

    def all(self)->str:
        result="{\"token\":\""+self.token+"\", \"directmessage\": \"all\"}"
        return result
    
    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages
        all_msg=self.all()
        self.client.sendall(all_msg.encode('utf-8'))
        rev_msg=self.client.recv(4096)
        DataTuple=ds_message_protocol.extract_json(rev_msg.decode('utf-8'))
        msgList=DataTuple.message
        print('msg', msgList)
        index=0
        returnList=[]
        while(index<len(msgList)):
            returnList.append(msgList[index])
            index+=1
        returnList = sorted(returnList, key = lambda x: x[0])
        #print(returnList)
        return returnList

#dm=DirectMessenger("168.235.86.101","blahblahblah", "hello")
if __name__ == '__main__':
    dm=DirectMessenger("168.235.86.101","newusercreated","strongpassword")
    dm2=DirectMessenger("168.235.86.101","guesswhat", "idk")

#print("send to blahblahblah", dm2.send("are you getting this blahblahblah?", "blahblahblah"))

#print("send to blahblahblah", dm2.send("are you getting this newusercreated test?", "newusercreated"))
#print("send to guesswhat", dm.send("are you getting this guesswhat test?", "guesswhat"))
#print("")
#print(dm2.send("Hello There!!!!", "blahblahblah"))
#print(dm.send("ugh!", "quesswhat"))
#print("dm.retrieve_new",dm.retrieve_new())
#print("")
#print("dm2.retrieve_new",dm2.retrieve_new())
#print("")
#print("guesswhat all",dm2.retrieve_all())
#print("")
#print("newusercreated all",dm.retrieve_all())
#print("")
#print("guesswhat all",dm2.retrieve_all())
#print("guesswhat new",dm2.retrieve_new())

'''
dm3=DirectMessenger()
print("dm.retrieve_new",dm3.retrieve_new())
print("")
print("dm.retrieve_all",dm3.retrieve_all())
'''

