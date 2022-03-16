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
        """
        Set self values to recieved values.
        """
        self.message=message
        self.recipient=recipient
        self.timestamp=str(time.time())


class DirectMessenger(DirectMessage):
    server="168.235.86.101"
    username="blahblahblah"
    password="hello"
    
    def __init__(self, dsuserver=None, username=None, password=None):
        super().__init__()
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
        DataTuple=ds_message_protocol.extract_json(rev_msg.decode('utf-8'))
        if (DataTuple.type!="error"):
            self.token=DataTuple.token


    def join(self)->str:
        """
        Join username, password, and empty token into one string.
        """
        result="{\"join\": {\"username\": \""+self.username+"\",\"password\": \""+self.password+"\",\"token\":\"""\"}}"
        return result


    def post(self)->str:
        """
        Returns token and directmessage, which contains message, recipient, and timestamp.
        """
        result="{\"token\":\""+self.token+"\", \"directmessage\": {\"entry\": \""+self.message+"\",\"recipient\":\""+self.recipient+"\", \"timestamp\": \""+self.timestamp+"\"}}"
        return result

    	
    def send(self, message:str, recipient:str) -> bool:
        """
        Returns true if message successfully sent, false if send failed.
        """
        super().set_message(message,recipient)
        validity=True
        postValid=True
        if (self.message!=""):
            post_msg=self.post()
            self.client.sendall(post_msg.encode('utf-8'))
            rev_msg=self.client.recv(4096)
            DataTuple=ds_message_protocol.extract_json(rev_msg.decode('utf-8'))
            if (DataTuple.type=="error"):
                validity=False
        else:
            postValid=False
        return validity and postValid
                

    def new(self)->str:
        """
        Generates a new string of token and directmessage(new).
        """
        result="{\"token\":\""+self.token+"\", \"directmessage\": \"new\"}"
        return result


    def retrieve_new(self) -> list:
        """
        Returns a list of DirectMessage objects containing all new messages
        """
        new_msg=self.new()
        self.client.sendall(new_msg.encode('utf-8'))
        rev_msg=self.client.recv(4096)
        DataTuple=ds_message_protocol.extract_json(rev_msg.decode('utf-8'))
        msgList=DataTuple.message
        index=0
        returnList=[]
        while(index<len(msgList)):
            returnList.append(msgList[index])
            index+=3
        return returnList


    def all(self)->str:
        """
        Generates a new string of token and directmessage(all).
        """
        result="{\"token\":\""+self.token+"\", \"directmessage\": \"all\"}"
        return result
    
    def retrieve_all(self) -> list:
        """
        Returns a list of DirectMessage objects containing all messages.
        """
        all_msg=self.all()
        self.client.sendall(all_msg.encode('utf-8'))
        rev_msg=self.client.recv(4096)
        DataTuple=ds_message_protocol.extract_json(rev_msg.decode('utf-8'))
        msgList=DataTuple.message
        index=0
        returnList=[]
        while(index<len(msgList)):
            returnList.append(msgList[index])
            index+=3
        return returnList


if __name__ == '__main__':
    dm=DirectMessenger("168.235.86.101","newusercreated","strongpassword")
    dm2=DirectMessenger("168.235.86.101","guesswhat", "idk")
