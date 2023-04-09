import re
import pymongo
from time import localtime, strftime
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, NumericProperty
import urllib
import json

myclient = pymongo.MongoClient("mongodb+srv://atta:190501@cluster0.zdkcp1y.mongodb.net/test")
mydb = myclient["vafa"]
myuser = mydb["user"]
myhis = mydb["history"]

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 13
        
class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 13

class Time(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 10
        
class MainApp(MDApp):
    current_id = ""
    
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signin.kv"))
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("history.kv"))
        return screen_manager
    
    def to_hist(self):
        screen_manager.transition.direction = "left"
        screen_manager.current = "hist"
        
    def to_sign(self):
        screen_manager.transition.direction = "left"
        screen_manager.current = "signin"
    
    def clear(self, screen):
        screen_manager.get_screen(screen).chat_list.clear_widgets()
            
    def to_login(self):
        screen_manager.transition.direction = "right"
        MainApp.current_id = ""
        screen_manager.current = "login"
        
    def to_main(self):
        if screen_manager.current == "login":
            screen_manager.transition.direction = "left"
        else:
            screen_manager.transition.direction = "right"
        screen_manager.current = "main"
        
    def signin(self, mail, passw, repassw):
        if MainApp.connect_test(self):
            myquery = {"mail": mail}
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if re.fullmatch(regex, mail):
                if len(passw) < 8:
                    toast("Password length must be greater than 8 !!!")
                else:
                    if repassw != passw:
                        toast("Different re-enter password !!!")
                    else:
                        if myuser.count_documents(myquery):
                            toast("This email is already registered !!!")
                        else:
                            user = {
                                "mail": mail,
                                "password": passw,
                            }
                            myuser.insert_one(user)
                            toast("Sign Up Success !!!")
                            MainApp.to_login(self)
            else:
                toast("Invalid email !!!")
            
    def check_login(self, mail, passw):
        if MainApp.connect_test(self):
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if re.fullmatch(regex, mail):
                if len(passw) < 8:
                    toast("Password length must be greater than 8 !!!")
                else:
                    myquery = {"mail": mail}
                    if myuser.count_documents(myquery):
                        user = myuser.find(myquery)[0]
                        if passw == user["password"]:
                            MainApp.current_id = user["_id"]
                            MainApp.to_main(self)
                        else:    
                            toast("Incorrect Password !!!")
                    else:
                        toast("Unregistered email !!!")
            else:
                toast("Invalid email !!!")
            
    def connect_test(self):
        try:
            response=urllib.request.urlopen('https://www.google.com/',timeout=1)
            return True
        except urllib.error.URLError as err:
            toast ("Can't connect to server! Please check your Internet!")
            return False
            
    def message(self, text):
        toast(text)
        
    def as_res(screen ,text):
        global size, halign
        if len(text) in range(0,11):
            size =.22
            halign="center"
        elif len(text) in range(11,21):
            size =.32
            halign="center"
        elif len(text) in range(21,31):
            size =.45
            halign="center"
        elif len(text) in range(31,41):
            size =.58
            halign="center"
        elif len(text) in range(41,51):
            size =.71
            halign="center"
        else:
            size = .9
            halign="justify"
        screen_manager.get_screen(screen).chat_list.add_widget(Response(text=text, size_hint_x=size, halign=halign))              
     
    def us_ques(screen, text):
        if len(text) in range(0,11):
            size =.22
            halign="center"
        elif len(text) in range(11,21):
            size =.32
            halign="center"
        elif len(text) in range(21,31):
            size =.45
            halign="center"
        elif len(text) in range(31,41):
            size =.58
            halign="center"
        elif len(text) in range(41,51):
            size =.71
            halign="center"
        else:
            size = .9
            halign="justify" 
        screen_manager.get_screen(screen).chat_list.add_widget(Command(text=text, size_hint_x=size, halign=halign))
        if screen == ("main"):
            screen_manager.get_screen(screen).scroll.scroll_y = 0.1
            
    def time_his(text):
        size = 1
        halign = "center"
        screen_manager.get_screen("hist").chat_list.add_widget(Time(text=text, size_hint_x=size, halign=halign))
            
    def load_his(self):
        
        myquery = {"id": MainApp.current_id}
        data = myhis.find(myquery)
        for doc in data:
            MainApp.time_his(doc["time"])
            MainApp.us_ques("hist", doc["question"])
            MainApp.as_res("hist", doc["response"])
            
         
    def chat_bot(self, question):
        if MainApp.connect_test(self):    
            headers = {
            'Authorization': "Bearer pk-tvCyIlXThuxlWPDsqwOJYTxLSQevKkXCrEANoIongjRdXbWh",
            'Content-Type': 'application/json',
            }

            json_data = {
                'model': 'gpt-3.5-turbo',
                'max_tokens': 4000,
                'stop': 'None',
                'messages': [
                    {
                        'role': 'user',
                        'content': question,
                    },
                ],
            }
            MainApp.us_ques("main", question)
            
            #get response from AI
            conditionsSetURL = 'https://api.pawan.krd/v1/chat/completions'
            params = json.dumps(json_data).encode('utf8')
            req = urllib.request.Request(conditionsSetURL, data=params,headers=headers)
            response = json.loads(urllib.request.urlopen(req).read().decode('utf8'))
                       
            try:
                data = response["choices"][0]["message"]
                if data["content"] == "":
                    MainApp.as_res("main", "I do not understand what you say! Can you be more specific again?")
                else:    
                    MainApp.as_res("main", data["content"])
                
                #push data to DB
                now = strftime("%H:%M:%S   %d/%m/%Y", localtime())
                history = {
                    "id": MainApp.current_id,
                    "question": question,
                    "response": data["content"],
                    "time": now,
                }
                myhis.insert_one(history)
            except:
                MainApp.as_res("main", "I do not understand what you say! Can you be more specific again?")
 
if __name__ == "__main__":
    MainApp().run()
