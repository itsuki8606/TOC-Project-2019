from transitions.extensions import GraphMachine

from utils import send_text_message,send_image_url,send_button_message
from crawler import list_all,search,search_article,search_author,search_score

key=''
start_url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
search_url = 'https://www.ptt.cc/bbs/Gossiping/search'

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_introduce(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'introduce'
        return False

    def is_going_to_list_all(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'list all'
        return False

    def is_going_to_search(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'search'
        return False

    def is_going_to_keyword_search(self, event):
        if event.get("message"):
            text = event['message']['text']
            global key
            key = text
            return True
            #return text.lower() == 'go to state3'
        return False

    def is_going_to_search_article(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'search article'
        return False

    def is_going_to_keyword_article(self, event):
        if event.get("message"):
            text = event['message']['text']
            global key
            key = text
            return True
            #return text.lower() == 'go to state3'
        return False

    def is_going_to_search_author(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'search author'
        return False

    def is_going_to_keyword_author(self, event):
        if event.get("message"):
            text = event['message']['text']
            global key
            key = text
            return True
            #return text.lower() == 'go to state3'
        return False

    def is_going_to_search_score(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'search score'
        return False

    def is_going_to_keyword_score(self, event):
        if event.get("message"):
            text = event['message']['text']
            global key
            key = text
            return True
            #return text.lower() == 'go to state3'
        return False

    def on_enter_introduce(self, event):
        print("I'm entering introduce")
        sender_id = event['sender']['id']
        send_image_url(sender_id, "https://i.imgur.com/8bZQa3w.jpg")
        send_button_message(sender_id, "查看簡介")
        self.go_back()

    def on_exit_introduce(self):
        print('Leaving introduce')

    def on_enter_list_all(self, event):
        print("I'm entering list_all")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "搜尋中，請稍後...")
        send_text_message(sender_id, list_all(start_url))
        self.go_back()

    def on_exit_list_all(self):
        print('Leaving list_all')

    def on_enter_search(self, event):
        print("I'm entering search")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "搜尋關鍵字")
        send_text_message(sender_id, "請輸入欲搜尋之關鍵字")
        #send_button_message(sender_id, "Test State2")
        #self.go_back()

    def on_exit_search(self,event):
        print('Leaving search')

    def on_enter_keyword_search(self, event):
        print("I'm entering keyword_search")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "搜尋中，請稍後...")
        send_text_message(sender_id, search(search_url,key))
        self.go_back()

    def on_exit_keyword_search(self):
        print('Leaving keyword_search')

    def on_enter_search_article(self, event):
        print("I'm entering search_article")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "搜尋文章")
        send_text_message(sender_id, "請輸入欲搜尋之文章名稱")
        #send_button_message(sender_id, "Test State2")
        #self.go_back()

    def on_exit_search_article(self,event):
        print('Leaving search_article')

    def on_enter_keyword_article(self, event):
        print("I'm entering keyword_article")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "搜尋中，請稍後...")
        send_text_message(sender_id, search_article(search_url,key))
        self.go_back()

    def on_exit_keyword_article(self):
        print('Leaving keyword_article')

    def on_enter_search_author(self, event):
        print("I'm entering search_author")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "搜尋作者")
        send_text_message(sender_id, "請輸入欲搜尋之作者名稱")
        #send_button_message(sender_id, "Test State2")
        #self.go_back()

    def on_exit_search_author(self,event):
        print('Leaving search_author')

    def on_enter_keyword_author(self, event):
        print("I'm entering keyword_author")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "搜尋中，請稍後...")
        send_text_message(sender_id, search_author(search_url,key))
        self.go_back()

    def on_exit_keyword_author(self):
        print('Leaving keyword_author')

    def on_enter_search_score(self, event):
        print("I'm entering search_score")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "搜尋推文數")
        send_text_message(sender_id, "請輸入欲搜尋之推文數")
        #send_button_message(sender_id, "Test State2")
        #self.go_back()

    def on_exit_search_score(self,event):
        print('Leaving search_score')

    def on_enter_keyword_score(self, event):
        print("I'm entering keyword_score")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "搜尋中，請稍後...")
        send_text_message(sender_id, search_score(search_url,key))
        self.go_back()

    def on_exit_keyword_score(self):
        print('Leaving keyword_score')
