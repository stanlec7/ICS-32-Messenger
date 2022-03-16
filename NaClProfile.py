# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin


# TODO: Install the pynacl library so that the following modules are available
# to your program.
# pip install pynacl

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
import unittest

import json, time, os
from pathlib import Path

# TODO: Import the Profile and Post classes
from Profile import Profile, Post, DsuFileError, DsuProfileError

# TODO: Import the NaClDSEncoder module
from NaClDSEncoder import NaClDSEncoder

# TODO: Subclass the Profile class 
class NaClProfile(Profile):
    def __init__(self):
        """
        TODO: Complete the initializer method. Your initializer should create the follow three 
        public data attributes:

        public_key:str
        private_key:str
        keypair:str

        Whether you include them in your parameter list is up to you. Your decision will frame 
        how you expect your class to be used though, so think it through.
        """
        super().__init__()
        self.public_key = ""
        self.private_key = ""
        self.keypair = ""

    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.

        TODO: Complete the generate_keypair method.

        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        :return: str    
        """

        nacl_enc = NaClDSEncoder()
        nacl_enc.generate()
        self.keypair = nacl_enc.keypair
        
        self.public_key = nacl_enc.public_key
        self.private_key = nacl_enc.private_key
        
        return self.keypair


    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.

        TODO: Complete the import_keypair method.

        This method should use the keypair parameter to populate the public data attributes created by
        the initializer. 
        
        NOTE: you can determine how to split a keypair by comparing the associated data attributes generated
        by the NaClDSEncoder
        """
        self.keypair = keypair
        self.public_key = keypair[:44]
        self.private_key = keypair[44:]


    def add_post(self, post: Post) -> None:
        """
        TODO: Override the add_post method to encrypt post entries.

        Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
        code that is already written in the parent class.

        NOTE: To call the method you are overriding as it exists in the parent class, you can use the built-in super keyword:
        
        super().add_post(...)
        """

        nacl = NaClDSEncoder()
        box = nacl.create_box(nacl.encode_private_key(self.private_key), nacl.encode_public_key(self.public_key))
        message = post.get_entry()
        message = nacl.encrypt_message(box, message)
        post = Post(message)
        super().add_post(post)


    def get_posts(self) -> list[Post]:
        """
        TODO: Override the get_posts method to decrypt post entries.

        Since posts will be encrypted when the add_post method is used, you will need to ensure they are 
        decrypted before returning them to the calling code.

        :return: Post
        
        NOTE: To call the method you are overriding as it exists in the parent class you can use the built-in super keyword:
        super().get_posts()
        """
        nacl = NaClDSEncoder()
        box = nacl.create_box(nacl.encode_private_key(self.private_key), nacl.encode_public_key(self.public_key))

        # LOWKEY WE DO NOT KNOW IF THIS IS RIGHT I AM PRETTY SURE NO BUT WE WILL SEE -stankey
        newlist = []

        for p in super().get_posts():
                new = Post(nacl.decrypt_message(box, p.get_entry()), p.get_time())
                newlist.append(new)
        return newlist
    

    def load_profile(self, path: str) -> None:
        """
        TODO: Override the load_profile method to add support for storing a keypair.

        Since the DS Server is now making use of encryption keys rather than username/password attributes, you will 
        need to add support for storing a keypair in a dsu file. The best way to do this is to override the 
        load_profile module and add any new attributes you wish to support.

        NOTE: The Profile class implementation of load_profile contains everything you need to complete this TODO.
        Just copy the code here and add support for your new attributes.
        """
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                try:
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.bio = obj['bio']
                    self.import_keypair(obj['keypair'])
                    for post_obj in obj['_posts']:
                        post = Post(post_obj['entry'], post_obj['timestamp'])
                        self._posts.append(post)
                except:
                    pass
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()


    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.
        
        TODO: Complete the encrypt_entry method.

        NOTE: A good design approach might be to create private encrypt and decrypt methods that your add_post, 
        get_posts and this method can call.
        
        :return: bytes 
        """
        nacl = NaClDSEncoder()
        box = nacl.create_box(nacl.encode_private_key(self.private_key), nacl.encode_public_key(public_key))
        message = nacl.encrypt_message(box, entry)
        return message

if __name__ == '__main__':
    np = NaClProfile()
    kp = np.generate_keypair()
    print(np.public_key)
    print(np.private_key)
    print(np.keypair)

    # Test encryption with 3rd party public key
    ds_pubkey = "jIqYIh2EDibk84rTp0yJcghTPxMWjtrt5NW4yPZk3Cw="
    ee = np.encrypt_entry("Encrypted Message for DS Server", ds_pubkey)
    print(ee)

    # Add a post to the profile and check that it is decrypted.
    np.add_post(Post("Hello Salted World!"))
    p_list = np.get_posts()
    print(p_list[0].get_entry())

    #C:\Users\stanl\Documents\ICS32\Assignments\Assignment5\mydsufile.dsu
    # Save the profile
    np.save_profile(r'C:\Users\stanl\Documents\ICS32\Assignments\Assignment5\assignment-5-encrypted-graphical-user-interface-stanlec7-main\mydsufile.dsu')

    print("Open DSU file to check if message is encrypted.")
    input("Press Enter to Continue")

    # Create a new NaClProfile object and load the dsu file.
    np2 = NaClProfile()
    np2.load_profile(r'C:\Users\stanl\Documents\ICS32\Assignments\Assignment5\assignment-5-encrypted-graphical-user-interface-stanlec7-main\mydsufile.dsu')
    # Import the keys
    np2.import_keypair(kp)

    # Verify the post decrypts properly
    p_list = np2.get_posts()
    print(p_list[0].get_entry())