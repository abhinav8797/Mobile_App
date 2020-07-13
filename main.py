from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


Builder.load_file('design.kv')

class LoginScreen(Screen):
    
    def login(self,uname,pword):
        if uname == '' or pword == '':  
            self.ids.login_wrong.text="username and password are required"  
        else:
            with open("users.json") as file:
                user = json.load(file)
            if uname in user and user[uname]['password']==pword:
                self.manager.current="success_login_screen"
                self.ids.username.text=""
                self.ids.password.text=""
                self.ids.login_wrong.text=""
            else:
                self.ids.login_wrong.text="Wrong username or password!"
                self.ids.username.text=""
                self.ids.password.text=""
            
    def forgot_pass(self):
        self.manager.current="forgot_pass_screen"
        self.ids.login_wrong.text=""
    
    def signup(self):
        self.manager.current="sign_up_screen"
        self.ids.login_wrong.text=""
   
    

class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        if uname == '' or pword == '':  
            self.ids.detailsrequired.text="username and password are required"
        else:
            with open("users.json") as file:
                users = json.load(file)
            if uname in users:
                self.ids.detailsrequired.text="username alredy exits"
                self.ids.username.text=""
                self.ids.password.text=""
            else:
                users[uname]={'username':uname,'password':pword,'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
                with open("users.json",'w') as file:
                    json.dump(users,file)
        
                self.manager.current="signup_success_screen"
                self.ids.username.text=""
                self.ids.password.text=""
                self.ids.detailsrequired.text=""

    #def login(self,uname,pword,detail):
    def login(self):
        self.manager.current="login_screen"
        self.ids.username.text=""
        self.ids.password.text=""
        self.ids.detailsrequired.text=""

class SignUpSuccessScreen(Screen):
    def go_to_login(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"
    

class ForgotPasswordScreen(Screen):
    
    def passchange(self,uname,npword,cpword):
        if uname == '' or npword == '' or cpword == '':  
            self.ids.username_wrong.text="username and password are required"
            #print(uname,npword,cpword)        
        
        else:
            with open("users.json") as file:
                user = json.load(file) 
            if uname in user and npword==cpword:
                user[uname]={'password':npword}
                with open("users.json",'w') as file:
                    json.dump(user,file)
                self.manager.current="pass_change_screen"
                self.ids.uname.text = ""
                self.ids.newpass.text = ""
                #print("erase")
                self.ids.cpass.text = ""
                #print("hello world")
                self.ids.username_wrong.text=""
            else:
                self.ids.username_wrong.text="Wrong username or password doesn't matched"

                self.ids.uname.text = ""
                self.ids.newpass.text = ""
                #print("hello worldll")
                self.ids.cpass.text = ""

    def login(self):
        self.manager.current="login_screen"
        self.ids.username_wrong.text=""
        self.ids.uname.text=""
        self.ids.newpass.text=""
        self.ids.cpass.text=""

class SuccessLoginScreen(Screen):
    def logout(self,feel):
        self.manager.transition.direction="right"
        #print(feel)
        self.manager.current="login_screen"
        self.ids.feeling.text = ""
        self.ids.quote.text=""
    
    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")
        
        available_feelings = [Path(filename).stem for filename in available_feelings]
        #print(available_feelings)
        #print(feel)
        if feel == '':  
            self.ids.quote.text="Enter your feeling "

        elif feel in available_feelings:
            with open(f"quotes/{feel}.txt",encoding="utf8") as file:
                quotes = file.readlines()
            #print(quotes)
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text ="Try another Feeling"
            self.ids.feeling.text="" 
    

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class PasswordChangeScreen(Screen):
    def login(self):
        self.manager.current="login_screen"

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()

