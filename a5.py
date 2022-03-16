
# a5.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.

#commentingggggg
#ghfhfgfhg
import tkinter as tk
from tkinter import ttk, filedialog
from Profile import Post, Profile
from NaClProfile import NaClProfile
from ds_messenger import DirectMessage, DirectMessenger


PORT = 3021
HOST="168.235.86.101"

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._posts = [Post]

        self._profiles=[Profile]
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
        self._current_user=None
        self.dm_dict={}
        self._my_pf=None
        self.dm=None

    def add_to_dm_dict(self, dm:DirectMessenger):
        self.dm_dict[dm.username] = dm

    def set_my_pf(self, pf:Profile,dm:DirectMessenger):
        self._my_pf=pf
        self.dm=dm

    def get_new_msg(self):
        textList=self.dm.retrieve_new()
        print('get_new_msg testList:', textList)
        for p in range(len(textList)):
            text=textList[p]
            self.viewer.insert(0.0, str(text)+"\n")

    
    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        print("index",index)
        entry = self._posts[index].entry
        print("entry", entry)
        self.set_text_entry(entry)

    def pf_node_select(self,entry):
        #print("is empty?", self.posts_tree.selection()[0])
        try:
            print("self.dm_dict",self.dm_dict)
            print(self.posts_tree.selection())
            index = int(self.posts_tree.selection()[0])
            entry=""
            error=False
            try:
                entry=self._profiles[index].username
            except:
                error=True
            if (error):
                entry=self._profiles[index]
            print("testing entry difference", entry) 
            #entry=self._profiles[index]
            
            print("pf username", entry)
            self._current_user=entry
            #dm=self.dm_dict[self._current_user]
            print("self._my_pf",self._my_pf)
            #dm=self.dm_dict[self._my_pf]
            print('here')
            #print("print dm",dm)
            print("self.dm",self.dm)
            self.set_view_when_click_pf(self.dm)
            #self.set_view_when_click_pf(entry)
        except:
            pass

    def set_view_when_click_pf(self,dm:DirectMessenger):
        print("inside set_view_when_click_pf")
        print("should be newusercreated dm", dm.username)
        textList=dm.retrieve_all()
        print(textList)
        for p in range(len(textList)):
            text=textList[p]
            print("text",text)
            self.viewer.insert(0.0, str(text)+"\n")
    
    """
    Returns the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        
        return self.entry_editor.get('1.0', 'end').rstrip()

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        # TODO: Write code to that deletes all current text in the self.entry_editor widget
        # and inserts the value contained within the text parameter.
        self.entry_editor.delete(0.0, 'end')
        self.entry_editor.insert(0.0, text)

    def reset_view(self,text:str):
        self.viewer.delete(0.0, 'end')
        self.viewer.insert(0.0, text)

    def set_view_entry(self, text:str):
        #self.viewer.delete(0.0, 'end')
        self.viewer.insert(0.0, text+"\n")
        self.entry_editor.delete(0.0, 'end')
        
        
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_posts(self, posts:list):
        # TODO: Write code to populate self._posts with the post data passed
        # in the posts parameter and repopulate the UI with the new post entries.
        # HINT: You will have to write the delete code yourself, but you can take 
        # advantage of the self.insert_posttree method for updating the posts_tree
        # widget.
        self._posts=posts
        for p in range(len(posts)):
            self.insert_post(posts[p])

    def set_profiles(self, pf:list):
        print("in set pf")
        self._profiles=pf
        print(len(pf))
        for p in range(len(pf)):
            self._profiles.append(pf[p])
            id = len(self._profiles) - 1
            print("index to be inserted at", id)
            if len(pf[p]) > 25:
                usr = usr[:24] + "..."
            
            self.posts_tree.insert('', id, id, text=pf[p])
            '''here should be guesswhat'''
            dm=DirectMessenger("168.235.86.101", "guesswhat","idk")
            self.add_to_dm_dict(dm)
            print("self.posts_tree")

    def insert_profile(self, pf:Profile):
        self._profiles.append(pf)
        id = len(self._profiles) - 1
        print("index to be inserted at", id)
        self._insert_profile_tree(id, pf)
        
        
    """
    Inserts a single post to the post_tree widget.
    """
    def insert_post(self, post: Post):
        self._posts.append(post)
        id = len(self._posts) - 1 #adjust id for 0-base of treeview widget
        self._insert_post_tree(id, post)
       # print("post inserted")


    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.set_text_entry("")
        self.reset_view("")
        #self.set_view_entry("HELLO")
        self.entry_editor.configure(state=tk.NORMAL)
        self.viewer.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_post_tree(self, id, post: Post):
        entry = post.entry
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."
        
        self.posts_tree.insert('', id, id, text=entry)

    def _insert_profile_tree(self, id, pf:Profile):
        usr=pf.username
        if len(usr) > 25:
            usr = usr[:24] + "..."
            
        self.posts_tree.insert('', id, id, text=usr)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.pf_node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="lightgrey")
        editor_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

        view_frame=tk.Frame(master=entry_frame, bg="lightgrey", height= 300)
        view_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=0)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=0, pady=0)
        self.entry_editor.place(x=0, y=0, height=100, width=500)

        self.viewer=tk.Text(view_frame, width=0)
        self.viewer.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=0, pady=0)
        self.viewer.place(x=0, y=10, height=350, width=500)

        
        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)
        entry_editor_scrollbar.place(x=0, y=100)

        viewer_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.viewer.yview)
        self.viewer['yscrollcommand'] = viewer_scrollbar.set
        viewer_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)
        viewer_scrollbar.place(x=0, y=10)
        

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, save_callback=None,online_callback=None,send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback= online_callback
        self._send_callback=send_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using he get() function:
        # chk_value = self.is_online.get()
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    """
    Calls the callback function specified in the online_callback class attribute, if
    available, when the chk_button widget has been clicked.
    """
    def online_click(self):
        # TODO: Add code that implements a callback to the chk_button click event.
        # The callback should support a single parameter that contains the value
        # of the self.is_online widget variable.
        if self._online_callback is not None:
            self._online_callback(self.is_online)
        #self._online_callback=self.is_online.get()

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def save_click(self):
        if self._save_callback is not None:
            self._save_callback()

    """
    Updates the text that is displayed in the footer_label widget
    """
    def set_status(self, message):
        self.footer_label.configure(text=message)

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        #save_button = tk.Button(master=self, text="Save Post", width=20)
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.configure(command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        self.chk_button.configure(command=self.online_click) 
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""
class MainApp(tk.Frame):
    
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = Profile()

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self._is_online=False
        self._profile_filename = None
        self.added_users=[Profile]
        #self.dm_dict={}
        self.dm=None


    """
    Creates a new DSU file when the 'New' menu item is clicked.
    """
    def new_profile(self):
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        self._profile_filename = filename.name

        # TODO Write code to perform whatever operations are necessary to prepare the UI for
        # a new DSU file.
        # HINT: You will probably need to do things like generate encryption keys and reset the ui.
        #self._current_profile = NaClProfile()

        self._current_profile = Profile()

        
        #self._current_profile.generate_keypair()
        '''here should be newusercreated '''
        self._current_profile.username="newusercreated"
        self._current_profile.password="strongpassword"
        self._current_profile.bio=None
        self.dm=DirectMessenger("168.235.86.101","newusercreated","strongpassword")
        self.body.reset_ui()
        self._current_profile.save_profile(self._profile_filename)
        self.body.set_my_pf(self._current_profile,self.dm)
        print("done new profile")


    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self):
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        # TODO: Write code to perform whatever operations are necessary to prepare the UI for
        # an existing DSU file.
        # HINT: You will probably need to do things like load a profile, import encryption keys 
        # and update the UI with posts.
        
        self._profile_filename = filename.name
        #self._current_profile = NaClProfile()
        self._current_profile = Profile()
        self._current_profile.dsuserver="168.235.86.101"
        '''here should be newusercreated'''
        self._current_profile.username="newusercreated"
        self._current_profile.password="strongpassword"
        self.dm=DirectMessenger("168.235.86.101","newusercreated","strongpassword")
        print("filename",self._profile_filename)
        #self._current_profile.save_profile(self._profile_filename)
        self._current_profile.load_profile(self._profile_filename)
        #self._current_profile.import_keypair(self._current_profile.keypair)
        self.body.reset_ui()
        
        #self.body.set_posts(self._current_profile.get_posts())
        #print("type test",type(self._current_profile.opened_profiles))
        #print("type inside list test",type(self._current_profile.opened_profiles[0]))
        #print(self._current_profile.opened_profiles)
        self.body.set_profiles(self._current_profile.opened_profiles)
        self.body.set_my_pf(self._current_profile,self.dm)
        #print("done?")


    def add_user(self):
        #print('in')
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        #print('filename',filename.name)
        pf=Profile()
        pf.dsuserver="168.235.86.101"
        '''here should be guesswhat'''
        pf.username="guesswhat"
        pf.password="idk"
        pf.save_profile(filename.name)
        #print('pf created going to load pf')
        pf.load_profile(filename.name)
        #print('loaded')
        self.added_users.append(pf)
        #print("pf added to list",self.added_users)
        #print(pf.username, pf.password)
        self.body.insert_profile(pf)
        #print("inserted to side")
        dm=DirectMessenger(pf.dsuserver,pf.username,pf.password)
        self.body.add_to_dm_dict(dm)
        #self.dm_dict[pf.username] = DirectMessenger(pf.dsuserver,pf.username,pf.password)
        self._current_profile.add_opened_profiles(pf.username)
        #print(self._current_profile.get_opened_profiles())
        #print(self._profile_filename)
        self._current_profile.save_profile(self._profile_filename)
        self._current_profile.load_profile(self._profile_filename)
        print(self._current_profile.get_opened_profiles())


        
    
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """
    def save_profile(self):
        # TODO: Write code to perform whatever operations are necessary to save a 
        # post entry when the user clicks the save_button widget.
        # HINT: You will probably need to do things like create a new Post object,
        # fill it with text, add it to the active profile, save the profile, and
        # clear the editor_entry UI for a new post.
        # This might also be a good place to check if the user has selected the online
        # checkbox and if so send the message to the server.
        post = Post(self.body.get_text_entry())
        self.body.insert_post(post)
        self._current_profile.add_post(post)
        self._current_profile.save_profile(self._profile_filename)
        #print("self._current_profile get Posts", self._current_profile.get_posts())
        #print("self.body.get_text_entry()",self.body.get_text_entry())
        #self._current_profile.load_profile(self._profile_filename)
        self.body.set_text_entry("")
        if self._is_online is True:
            self.publish(post)

    def send_msg(self):
        msg=self.body.get_text_entry()
        print('set view entry')
        self.body.set_view_entry(msg)
        #print(self.body.pf_node_select())
        print("_current_user should be guesswhat", self.body._current_user)
        self.dm.send(msg,self.body._current_user)
        print("in send msg",self._current_profile.get_opened_profiles())
        
        

    def publish(self, post:Post):
        #print(self._current_profile)
        '''
        usr=self._current_profile.username
        pwd=self._current_profile.password
        bio=self._current_profile.bio
        #print(usr, pwd, bio)
        '''
        #print("post.get_entry()", post.get_entry())
        #print(ds_client.send(HOST, PORT, usr, pwd, post.get_entry(),bio))
        #print(ds_client.send(self._current_profile,post))
        ds_client.send(self._current_profile,post)

        
        

    """
    A callback function for responding to changes to the online chk_button.
    """
    def online_changed(self, value:bool):
        # TODO: 
        # 1. Remove the existing code. It has been left here to demonstrate
        # how to change the text displayed in the footer_label widget and
        # assist you with testing the callback functionality (if the footer_label
        # text changes when you click the chk_button widget, your callback is working!).
        # 2. Write code to support only sending posts to the DSU server when the online chk_button
        # is checked.
        #print("type", type(value))
        #print(value)
        #print("value",value.get())
        self._is_online=(value.get()==1)
        #print(self._is_online)
        #self.body.set_text_entry("Hello World")
        #self.new_profile()
        #self.open_profile()
        if value.get() == 1:
            #print('IN')
            self.footer.set_status("Online")
        else:
            self.footer.set_status("Offline")

    #def send_to_rec(self):
        
        
    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        menu_file.add_command(label='Add User', command=self.add_user)
        
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, save_callback=self.save_profile, online_callback=self.online_changed,send_callback=self.send_msg)
        #self.online_changed(self.footer.online_click())
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

    def check_new_msg(self):
        # perform some operation
        print("being called?")
        try:
            self.body.get_new_msg()
        except:
            pass
        finally:
            self.root.after(5000,self.check_new_msg)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    main.configure(bg='blue')

    app=MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    #print("__main__")
    main.after(5000, app.check_new_msg)
    
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
