
# a5.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.

import tkinter as tk
from tkinter import ttk, filedialog
from Profile import Post, Profile
from NaClProfile import NaClProfile
from ds_messenger import DirectMessage, DirectMessenger


PORT = 3021
HOST="168.235.86.101"

class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self._posts = [Post]
        self._profiles=[Profile]
        self.firstDraw=True
        self.night=None
        self._draw()
        self._current_user=None
        self.dm_dict={}
        self.rec_dm=None
        self._my_pf=None
        self.dm=None

    def add_to_dm_dict(self, dm:DirectMessenger):
        self.dm_dict[dm.username] = dm

    def set_my_pf(self, pf:Profile,dm:DirectMessenger):
        self._my_pf=pf
        self.dm=dm

    def get_new_msg(self):
        """
        Gets list of tuples, send user's username and user's message to set_view_entry()
        """
        textList=self.dm.retrieve_new()
        for p in range(len(textList)):
            text=textList[p][2]
            self.set_view_entry(str(text), textList[p][1])

    
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._posts[index].entry
        self.set_text_entry(entry)


    def pf_node_select(self,entry):
        try:
            index = int(self.posts_tree.selection()[0])
            entry=""
            error=False
            try:
                entry=self._profiles[index].username
            except:
                error=True
            if (error):
                entry=self._profiles[index]
            self._current_user=entry
            self.set_view_when_click_pf(self.dm)
        except:
            pass


    def set_view_when_click_pf(self,dm:DirectMessenger):
        """
        When a profile has been clicked, open the dm
        """
        textList=dm.retrieve_all()
        recipientDm = DirectMessenger("168.235.86.101","newestuser2", "verystrongpwd2")
        textListRecipient=recipientDm.retrieve_all()
        allText=textList + textListRecipient
        allText.sort(key=lambda tup:tup[0])
        for p in range(len(allText)):
            text=allText[p][2]
            self.set_view_entry(str(text), allText[p][1])
    
    
    def get_text_entry(self) -> str:
        """
        Returns the text that is currently displayed in the entry_editor widget.
        """ 
        return self.entry_editor.get('1.0', 'end').rstrip()


    def set_text_entry(self, text:str):
        """
        Sets the text to be displayed in the entry_editor widget.
        """
        self.entry_editor.delete(0.0, 'end')
        self.entry_editor.insert(0.0, text)


    def reset_view(self,text:str):
        """
        Resets the message display window.
        """
        self.viewer.delete(0.0, 'end')
        self.viewer.insert(0.0, text)


    def set_view_entry(self, text:str, user=None):
        """
        Displays the user's and the corresponding message: f'{user}: {text}'.
        """
        if user == None:
            printed=f'newestuser1: {text}'
        else:
            printed = f'{user}: {text}'
        self.viewer.insert("end", printed+"\n")
        self.entry_editor.delete(0.0, 'end')
        
    
    def set_posts(self, posts:list):
        """
        Set self._posts to the posts being passed in.
        Repopulate the UI with the new post entries.
        """
        self._posts=posts


    def set_profiles(self, pf:list):
        """
        Sets up profiles of the retrievers.
        """
        self._profiles=pf
        for p in range(len(pf)):
            self._profiles.append(pf[p])
            id = len(self._profiles) - 1
            if len(pf[p]) > 25:
                usr = usr[:24] + "..."
            self.posts_tree.insert('', id, id, text=pf[p])
            self.rec_dm=DirectMessenger("168.235.86.101", "newestuser2","verystrongpwd2")


    def insert_profile(self, pf:Profile):
        """
        Insert the retrievers user in the selection menu.
        """
        self._profiles.append(pf)
        id = len(self._profiles) - 1
        self._insert_profile_tree(id, pf)
        
        
    def insert_post(self, post: Post):    
        """
        Inserts a single post to the post_tree widget.
        """
        self._posts.append(post)
        id = len(self._posts) - 1
        self._insert_post_tree(id, post)

    
    def reset_ui(self):
        """
        Resets all UI widgets to their default state.
        """
        self.set_text_entry("")
        self.reset_view("")
        self.entry_editor.configure(state=tk.NORMAL)
        self.viewer.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    
    def _insert_post_tree(self, id, post: Post):
        """
        Inserts a post entry into the posts_tree widget.
        """
        entry = post.entry
        if len(entry) > 25:
            entry = entry[:24] + "..."
        self.posts_tree.insert('', id, id, text=entry)


    def _insert_profile_tree(self, id, pf:Profile):
        """
        Inserts a profile into the posts_tree widget.
        """
        usr=pf.username
        if len(usr) > 25:
            usr = usr[:24] + "..."
        self.posts_tree.insert('', id, id, text=usr)


    def _body_to_night(self):
        """
        Sets body to night mode
        """
        self.night=True
        self._draw()


    def _body_to_night_off(self):
        """
        Turn off night.
        """
        self.night=False
        self._draw()
    
    
    def _draw(self):
        """
        Draws the windows of the messenger.
        """
        style=ttk.Style()
        if (self.firstDraw):
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
            self.entry_editor.place(x=0, y=0, height=60, width=500) #edit
            self.viewer=tk.Text(view_frame, width=0)
            self.viewer.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=0, pady=0)
            self.viewer.place(x=0, y=10, height=350, width=500)
            self.viewer.tag_config('my retrieve', foreground="red")
            self.viewer.tag_config('recipient retrieve', foreground="red")
            entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
            self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
            entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)
            entry_editor_scrollbar.place(x=0, y=100)
            viewer_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.viewer.yview)
            self.viewer['yscrollcommand'] = viewer_scrollbar.set
            viewer_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)
            viewer_scrollbar.place(x=0, y=10)
            self.firstDraw=False
        else:
            if(self.night):
                style.configure("Treeview", background="grey", fieldbackground="grey")
                self.entry_editor.config(bg="grey")
                self.viewer.config(bg="grey")
            if(not self.night):
                style.configure("Treeview", background="white", fieldbackground="white")
                self.entry_editor.config(bg="white")
                self.viewer.config(bg="white")
        

class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, save_callback=None,online_callback=None,send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback= online_callback
        self._send_callback=send_callback
        self.is_online = tk.IntVar()
        self._draw()
    
    
    def online_click(self):
        """
        Calls the callback function specified in the online_callback class attribute, if
        available, when the chk_button widget has been clicked.
        """
        if self._online_callback is not None:
            self._online_callback(self.is_online)


    def save_click(self):
        """
        Calls the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._save_callback is not None:
            self._save_callback()

    
    def set_status(self, message):
        """
        Updates the text that is displayed in the footer_label widget
        """
        self.footer_label.configure(text=message)


    def send_click(self):
        """
        Send is click, call send_callback
        """
        if self._send_callback is not None:
            self._send_callback()
    
  
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.configure(command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NightLight():
    """
    Returns true for night on or night off
    """

    def night_on(self):
        """
        True for night on
        """
        return True
        

    def night_off(self):
        """
        True for night off
        """
        return True


class MainApp(tk.Frame, NightLight):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the NaClProfile class.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._current_profile = Profile()
        self._draw()
        self._is_online=False
        self._profile_filename = None
        self.added_users=[Profile]
        self.dm=None
    

    def new_profile(self):
        """
        Creates a new DSU file when the 'New' menu item is clicked.
        """
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        self._profile_filename = filename.name
        self._current_profile = Profile()
        self._current_profile.username="newestuser"
        self._current_profile.password="verystrongpwd"
        self._current_profile.bio=None
        self.dm=DirectMessenger("168.235.86.101","newestuser","verystrongpwd")
        self.body.reset_ui()
        self._current_profile.save_profile(self._profile_filename)
        self.body.set_my_pf(self._current_profile,self.dm)


    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        self._profile_filename = filename.name
        self._current_profile = Profile()
        self._current_profile.dsuserver="168.235.86.101"
        self._current_profile.username="newestuser"
        self._current_profile.password="verystrongpwd"
        self.dm=DirectMessenger("168.235.86.101","newestuser","verystrongpwd")
        self._current_profile.load_profile(self._profile_filename)
        self.body.reset_ui()
        self.body.set_profiles(self._current_profile.opened_profiles)
        self.body.set_my_pf(self._current_profile,self.dm)


    def add_user(self):
        """
        Adds a user named "newstuser2".
        """
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        pf=Profile()
        pf.dsuserver="168.235.86.101"
        pf.username="newestuser2"
        pf.password="verystrongpwd2"
        pf.save_profile(filename.name)
        pf.load_profile(filename.name)
        self.added_users.append(pf)
        self.body.insert_profile(pf)
        dm=DirectMessenger(pf.dsuserver,pf.username,pf.password)
        self.body.add_to_dm_dict(dm)
        self._current_profile.add_opened_profiles(pf.username)
        self._current_profile.save_profile(self._profile_filename)
        self._current_profile.load_profile(self._profile_filename)

    
    def close(self):
        """
        Closes the program when the 'Close' menu item is clicked.
        """
        self.root.destroy()

    
    def save_profile(self):
        """
        Saves the text currently in the entry_editor widget to the active DSU file.
        """
        post = Post(self.body.get_text_entry())
        self.body.insert_post(post)
        self._current_profile.add_post(post)
        self._current_profile.save_profile(self._profile_filename)
        self.body.set_text_entry("")
        if self._is_online is True:
            self.publish(post)

    def send_msg(self):
        """
        Send message
        """
        msg=self.body.get_text_entry()
        self.dm.send(msg,self.body._current_user)
        self.body.set_view_entry(msg)
        
        
    def publish(self, post:Post):
        """
        Publish the posts w current profile
        """
        ds_client.send(self._current_profile,post)

        
    def online_changed(self, value:bool):
        """
        A callback function for responding to changes to the online chk_button.
        """
        self._is_online=(value.get()==1)
        if value.get() == 1:
            self.footer.set_status("Online")
        else:
            self.footer.set_status("Offline")


    def night_true(self):
        """
        Turn on night mode.
        """
        if NightLight.night_on:
            self.footer.config(bg="grey")
            self.body._body_to_night()
        

    def night_false(self):
        """
        Turn off night mode.
        """
        if NightLight.night_off:
            self.footer.config(bg="")
            self.body._body_to_night_off()      
        

    def _draw(self):
        """
        Build a menu and add it to the root frame.
        """
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        menu_file.add_command(label='Add User', command=self.add_user)
        options_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=options_menu, label='Options')
        if NightLight.night_on == True:
            cmd=self.night_true()
        elif NightLight.night_off == True:
            cmd=self.night_false()
        options_menu.add_command(label='Night Mode On', command=self.night_true)
        options_menu.add_command(label='Night Mode Off', command=self.night_false)
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, save_callback=self.save_profile, online_callback=self.online_changed,send_callback=self.send_msg)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


    def check_new_msg(self):
        """
        Checks new message.
        """
        try:
            self.body.get_new_msg()
        except:
            pass
        finally:
            self.root.after(5000,self.check_new_msg)



if __name__ == "__main__":
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Demo")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    main.configure(bg='blue')
    app=MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.after(5000, app.check_new_msg)
    main.mainloop()
