from transitions.extensions import GraphMachine

from utils import send_text_message,send_image_url,send_button_message
from crawler import search,search_article,search_author,search_recommend

key=''

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_state1(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state1'
        return False

    def is_going_to_state2(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state2'
        return False

    def is_going_to_state3(self, event):
        if event.get("message"):
            text = event['message']['text']
            global key
            key = text
            return True
            #return text.lower() == 'go to state3'
        return False

    def on_enter_state1(self, event):
        print("I'm entering state1")
        sender_id = event['sender']['id']
        send_image_url(sender_id, "https://i.imgur.com/8bZQa3w.jpg")
        self.go_back()

    def on_exit_state1(self):
        print('Leaving state1')

    def on_enter_state2(self, event):
        print("I'm entering state2")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "關鍵字查詢")
        send_button_message(sender_id, "Test State2")
        #self.go_back()

    def on_exit_state2(self,event):
        print('Leaving state2')

    def on_enter_state3(self, event):
        print("I'm entering state3")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "請稍後")
        search_url = 'https://www.ptt.cc/bbs/Gossiping/search'
        send_text_message(sender_id, search(search_url,key))
        self.go_back()

    def on_exit_state3(self):
        print('Leaving state3')
