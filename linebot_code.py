from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage

app = Flask(__name__)

@app.route("/", methods=['POST'])
# 裝飾器是告訴 Flask，哪個 URL 應該觸發我們的函式。
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = 'fic8a+ZLfMsqOfw+jEIO2HmDFa43j6wC8DgxqHfO+ozSTNugq1BEj3aNYVPX6vpG58csSP3PmeHbQrY/vOnWKGy75rfTKvUx8EqDJOC3DiRWoEpy6EZJw3NBPaKaSZRmhdAeV8PCYljC1bvPu2dfvwdB04t89/1O/w1cDnyilFU='
        secret = 'b788548b94e7e881a3794b7503effc36'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型

        stickerId = json_data['events'][0]['message']['stickerId'] # 取得 stickerId
        packageId = json_data['events'][0]['message']['packageId'] # 取得 packageId
        

        print("This is json_data", json_data)
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            print(msg)                                       # 印出內容
            reply = msg
            line_bot_api.reply_message(tk, TextSendMessage(text=reply))# 回傳訊息
        elif type=='sticker':
            sticker_message = StickerSendMessage(sticker_id=stickerId, package_id=packageId) # 設定要回傳的表情貼圖
            line_bot_api.reply_message(tk, sticker_message)  # 回傳訊息
        else:
            reply = '你傳的不是文字呦～'
            line_bot_api.reply_message(tk, TextSendMessage(text=reply))# 回傳訊息
        
        print(reply)
        
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    app.run()