import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, MessageTemplateAction

from fsm import TocMachine
from utils import send_text_message, send_button_message, send_image_message


load_dotenv()


machine = TocMachine(
    states=[
        'user',
        'menu',
        'choose_genre',
        'coming_soon_drama',
        'trivia',
        'fsm',
        'option_actor',
        'choose_actor',
        'option_years',
        'choose_years',
        'final',
    ],
    transitions=[
        {'trigger': 'advance', 'source': 'user', 'dest': 'menu', 'conditions': 'is_going_to_menu'},

        {'trigger': 'advance', 'source': 'menu', 'dest': 'choose_genre', 'conditions': 'is_going_to_choose_genre'},
        {'trigger': 'advance', 'source': 'menu', 'dest': 'coming_soon_drama', 'conditions': 'is_going_to_coming_soon_drama'},
        {'trigger': 'advance', 'source': 'menu', 'dest': 'trivia', 'conditions': 'is_going_to_trivia'},
        {'trigger': 'advance', 'source': 'menu', 'dest': 'fsm', 'conditions': 'is_going_to_fsm'},

        {'trigger': 'advance', 'source': 'choose_genre', 'dest': 'option_actor', 'conditions': 'is_going_to_option_actor'}, #確認要不要選演員
        {'trigger': 'advance', 'source': 'option_actor', 'dest': 'choose_actor', 'conditions': 'is_going_to_choose_actor'}, #選演員
        {'trigger': 'advance', 'source': 'option_actor', 'dest': 'final', 'conditions': 'is_going_to_final'}, #直接推薦，不選演員

        {'trigger': 'advance', 'source': 'choose_actor', 'dest': 'option_years', 'conditions': 'is_going_to_option_years'}, #確認要不要選年份
        {'trigger': 'advance', 'source': 'option_years', 'dest': 'choose_years', 'conditions': 'is_going_to_choose_years'}, #選發行年份
        {'trigger': 'advance', 'source': 'option_years', 'dest': 'final', 'conditions': 'is_going_to_final'}, #直接推薦，不選年份

        {'trigger': 'advance', 'source': 'choose_actor', 'dest': 'choose_genre', 'conditions': 'is_going_to_choose_genre'}, #若找不到演員出演的韓劇有此類型
        
        {'trigger': 'advance', 'source': 'choose_years', 'dest': 'final', 'conditions': 'is_going_to_final'}, #直接推薦，不選年份
        {
            'trigger': 'go_back',
            'source': [
                'coming_soon_drama',
                'trivia',
                'final',
            ],
            'dest': 'user'
        },
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path='')


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route('/callback', methods=['POST'])
def webhook_handler():
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')
        response = machine.advance(event) # 從fsm.py的每個on_enter得來
        if response == False:
            # send_text_message(event.reply_token, "請依照指示與按鈕來操作!")
            # send_text_message(event.reply_token, '歡迎來到韓劇小幫手\n推薦給你最好看最吸睛的韓劇❤️❤️❤️\n這邊可以根據『類型』、『演員』、『發行年份』找出最適合你的韓劇唷🥳\n輸入『start』就可以根據你的喜好挑選囉~')


            if machine.state == 'user':
                text = '按下『推薦經典韓劇』會根據“類型”、“演員”、“發行年份”找出最適合你的韓劇🥳\n按下『即將上檔韓劇』了解更多即將開播的韓劇🤤\n按下『關於韓劇的冷知識』可以知道看了那麼多韓劇都沒發現的冷知識🥴\n按下『FSM』可以得到當下的狀態圖唷😏！！！！！現在輸入『start』就準備進入韓劇小天地囉🥰！！！！！'
                send_text_message(event.reply_token, text)
            # if machine.state == 'final' or machine.state == 'coming_soon_drama' or machine.state == 'trivia':
            #     text = '按下『推薦經典韓劇』會根據“類型”、“演員”、“發行年份”找出最適合你的韓劇🥳\n按下『即將上檔韓劇』了解更多即將開播的韓劇🤤\n按下『關於韓劇的冷知識』可以知道看了那麼多韓劇都沒發現的冷知識唷🥴\n！！！！！現在輸入『start』就準備進入韓劇小天地囉🥰！！！！！'
            #     send_text_message(event.reply_token, text)

    return 'OK'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return send_file('fsm.png', mimetype='image/png')


if __name__ == '__main__':
    port = os.environ.get('PORT', 8000)
    app.run(host='0.0.0.0', port=port, debug=True)
