from transitions.extensions import GraphMachine
from utils import send_text_message, send_button_message, send_image_message, send_image_carousel_message, send_confirm_message, send_carousel_message
from bs4 import BeautifulSoup
import requests
from linebot.models import MessageTemplateAction
import pandas as pd

# global variable
option = ''
genre = ''
actor = ''
years = 0
df = pd.read_csv('drama.csv')
df_new = pd.read_csv('new_drama.csv')

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs) #建立fsm

    # user start
    def is_going_to_menu(self, event):
        text = event.message.text
        if text == 'start':
            return True
        return False

    def is_going_to_choose_genre(self, event): #走到choose_genre這個state時 要做的動作
        text = event.message.text
        if text == '推薦經典韓劇':
            return True
        if text == 'back' and self.state == 'choose_actor': #從choose_actor回來
            return True
        return False

    def is_going_to_coming_soon_drama(self, event):
        text = event.message.text
        if text == '即將上檔韓劇':
            return True
        return False

    def is_going_to_trivia(self, event):
        text = event.message.text
        if text == '關於韓劇的冷知識':
            return True
        return False

    def is_going_to_fsm(self, event):
        text = event.message.text
        if text == 'FSM':
            return True
        return False

    def is_going_to_option_actor(self, event): #從choose_genre走到option_actor時,要確認是哪種類型韓劇,才能進到下一個state
        global genre #10種
        text = event.message.text
        if text == '喜劇':
            genre = '喜劇'
            return True
        elif text == '動作':
            genre = '動作'
            return True
        elif text == "狗血":
            genre = '狗血'
            return True
        elif text == '愛情':
            genre = '愛情'
            return True
        elif text == '校園':
            genre = '校園'
            return True
        elif text == '犯罪':
            genre = '犯罪'
            return True
        elif text == '懸疑':
            genre = '懸疑'
            return True
        elif text == '奇幻':
            genre = '奇幻'
            return True
        elif text == '古裝':
            genre = '古裝'
            return True
        elif text == '驚悚':
            genre = '驚悚'
            return True
        return False #會印出app.py(machine.state == 'choose_genre')時的所寫的字

    def is_going_to_choose_actor(self, event):
        text = event.message.text 
        if text == 'continue':
            return True
        return False
            
    def is_going_to_option_years(self, event): #往option_year的路上->確認演員名稱
        global actor, genre
        text = event.message.text
        if text != 'back': #輸入back->在走的時候會兩條路(is_going_to_choose&is_going_option_years)都符合->return2次
            df_actor = df[ df['演員名稱'].str.contains(text)] #contains: 確認string裡有無substring
            df_check = df[ df['類型'].str.contains(genre) & df['演員名稱'].str.contains(text)]
            if len(df_actor) == 0:
                text = '找不到任何這個演員的出演的韓劇😥\n請再輸入一次演員名稱!!'
                send_text_message(event.reply_token, text)
                return False
            elif len(df_check) == 0:
                text = '找不到此演員出演的韓劇中有包括"'+ genre +'"類型的韓劇😥\n請再輸入一次演員名稱!!\n或者輸入『back』重新選擇其他的韓劇類型!!'
                send_text_message(event.reply_token, text)
                return False
            else:
                actor = text
                return True

    def is_going_to_choose_years(self, event):
        text = event.message.text 
        if text == 'continue': #若要接著繼續選若要接著繼續選發行年份
            return True
        return False

    def is_going_to_final(self, event):
        global years
        text = event.message.text
        if text == 'skip': #直接推薦
            return True
        elif text.lower().isnumeric(): #到最後輸入年份時
            years = int(text)
            if years >=2020 and years <=2022:
                return True
        return False

    # def on_enter_user(self, event):
    #     if self.state=='final' or self.state=='coming_soon_drama' or self.state=='trivia':
    #         text = '按下『推薦經典韓劇』會根據“類型”、“演員”、“發行年份”找出最適合你的韓劇🥳\n按下『即將上檔韓劇』了解更多即將開播的韓劇🤤\n按下『關於韓劇的冷知識』可以知道看了那麼多韓劇都沒發現的冷知識唷🥴\n！！！！！現在輸入『start』就準備進入韓劇小天地囉🥰！！！！！'
    #         send_text_message(event.reply_token, text)

    def on_enter_menu(self, event):
        title = '韓劇小幫手😇'
        text = '根據上述的提示來操作唷~'
        url = 'https://a.ksd-i.com/a/2020-06-03/127239-844836.jpg'
        option1 = MessageTemplateAction(label = '推薦經典韓劇', text = '推薦經典韓劇')
        option2 = MessageTemplateAction(label = '即將上檔韓劇', text = '即將上檔韓劇')
        option3 = MessageTemplateAction(label = '關於韓劇的冷知識', text = '關於韓劇的冷知識')
        option4 = MessageTemplateAction(label = 'FSM', text = 'FSM')
        buttons = [option1, option2, option3, option4]
        send_button_message(event.reply_token, title, text, buttons, url)

    def on_enter_choose_genre(self, event):
        titles = ['喜劇', '動作', '愛情', '狗血', '校園', '犯罪', '日常', '奇幻', '古裝', '驚悚']
        texts = titles
        url1 = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/cats-1657605927.jpg?crop=0.497xw:0.993xh;0,0&resize=640:*'
        url2 = 'https://a.ksd-i.com/a/2022-10-12/143841-955867.jpg'
        url3 = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/c2-1642757268.jpg?crop=0.491xw:0.980xh;0.506xw,0.0130xh&resize=640:*'
        url4 = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/try3-1585646856.png?crop=0.502xw:1.00xh;0.500xw,0&resize=640:*'
        url5 = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/fotojet-2-1642174387.jpg?crop=0.498xw:0.997xh;0.502xw,0&resize=640:*'
        url6 = 'https://pic.pimg.tw/myfairystory/1620872905-1165731990-g.jpg'
        url7 = 'https://a.ksd-i.com/a/2021-09-14/137491-918907.jpg'
        url8 = 'https://cdn.hk01.com/di/media/images/3132804/org/f9ff18b8ca957398e385bf710b587ca4.jpg/K0I8JqgP9MkfWEHAPMMA8Q5BPQL12_oHh5wVEYecFRE?v=w1920'
        url9 = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/402-1604297990.jpg?crop=1.00xw:0.767xh;0,0.137xh&resize=480:*'
        url10 = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/f637497689666905146.jpg'
        image_links = [url1, url2, url3, url4, url5, url6, url7, url8, url9, url10]
        send_image_carousel_message(event.reply_token, titles, texts, image_links)

    def on_enter_coming_soon_drama(self, event):
        titles = []
        image_links = []
        url_links = []
        for index, row in df_new.iterrows():
            print(index)
            print(row)
            titles.append(row['韓劇名稱'])
            image_links.append(row['圖片'])
            url_links.append(row['預告'])
        send_carousel_message(event.reply_token, titles, image_links, url_links)
        self.go_back(event)

    def on_enter_trivia(self, event):
        text = '看韓劇教我們關於韓國的冷知識🥶😳\n'
        text += '1. 掛電話前不說掰掰📞\n在台灣掛電話之前一定會說一句「掰掰」、「再見」，要是沒說就是不禮貌。而韓國則是習慣用「語助詞」作為電話的結尾，對他們而言，反而說掰掰是件失禮的事。\n'
        text += '2. 南男北女(남남북녀)\n是韓國一句俗諺語，大意是指：男人是南邊的更帥；女人則是北邊的最美。\n'
        text += '3. 炸啤(치맥)\n炸雞跟啤酒的簡寫。因為來自星星的你所帶來的炸啤旋風\n'
        text += '4. 三溫暖的羊角頭巾♨️\n因為在溫度比較高的地方會流汗，容易導致身體處於黏糊糊的狀態，所以才會用毛巾把頭包成羊咩咩頭，汗就不會一直滴下來！\n'
        text += '5. 最長壽的韓劇👨🏻‍🦳\n1980播出的《田園日記》，竟一路播了22年，到了2002年才正式完結！'
        send_text_message(event.reply_token, text)
        self.go_back(event) #回到初始狀態

    def on_enter_fsm(self, event):
        url = 'https://f2d6-2401-e180-8864-3610-d1c3-5bcc-b9e7-f60c.jp.ngrok.io/show-fsm'
        # send_image_message(event.reply_token, 'https://a.ksd-i.com/a/2022-10-12/143841-955867.jpg')
        send_image_message(event.reply_token, url)

    def on_enter_option_actor(self, event): #決定要選演員或是不選演員
        text = '請選擇是否有想看的特定演員!\n按下『continue』挑選出演演員\n按下『skip』直接推薦給您韓劇'
        pick_button = [MessageTemplateAction(label='continue', text='continue'), MessageTemplateAction(label='skip', text='skip')]
        send_confirm_message(event.reply_token, text, pick_button)

    def on_enter_choose_actor(self, event):
        send_text_message(event.reply_token, '請輸入你喜歡的演員名字')
    
    def on_enter_option_years(self, event): #決定要選演員或是不選演員
        text = '請選擇是否要推薦特定發行年份的韓劇\n按下『continue』挑選年份\n按下『skip』直接推薦給您韓劇'
        pick_button = [MessageTemplateAction(label='continue', text='continue'), MessageTemplateAction(label='skip', text='skip')]
        send_confirm_message(event.reply_token, text, pick_button)

    def on_enter_choose_years(self, event):
        send_text_message(event.reply_token, '請輸入你想搜尋的韓劇發行年份(2020-2022)')

    def on_enter_final(self, event):
        global genre, actor, years
        if actor=='' and years == 0: #option_actor直接跳到final時->只根據類型選擇
            fit_drama = df[ df['類型'].str.contains(genre) ] 
        elif years == 0: #option_years直接跳到final時
            fit_drama = df[ df['類型'].str.contains(genre) & df['演員名稱'].str.contains(actor) ]
        else:
            fit_drama = df[ df['類型'].str.contains(genre) & df['演員名稱'].str.contains(actor) & (df['發行年份']==years) ]

        #前面的state已經檢查過是否有包含這演員...->不需再檢查一次
        titles = []
        image_links = []
        url_links = []
        recommend_drama = fit_drama.head(3) # 推薦前三部
        for index, row in recommend_drama.iterrows():
            titles.append(row['韓劇名稱'])
            image_links.append(row['圖片'])
            url_links.append(row['預告'])
        send_carousel_message(event.reply_token, titles, image_links, url_links)
        self.go_back(event) #回到初始狀態
        