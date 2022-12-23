import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, ConfirmTemplate, ButtonsTemplate, MessageTemplateAction, ImageSendMessage, URIAction, CarouselTemplate, CarouselColumn

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def send_text_message(reply_token, text): #要傳送的訊息:text
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(reply_token, title, text, buttons, url): #url:網址
    line_bot_api = LineBotApi(channel_access_token)
    botton_template = ButtonsTemplate(title=title, text=text, thumbnail_image_url = url, actions = buttons)
    message = TemplateSendMessage(alt_text='button template', template = botton_template)
    line_bot_api.reply_message(reply_token, message)
    
    return "OK"

def send_confirm_message(reply_token, text, buttons):
    line_bot_api = LineBotApi(channel_access_token)
    confirm_template = ConfirmTemplate(text=text, actions=buttons)
    message = TemplateSendMessage(alt_text='confirm template', template=confirm_template)
    line_bot_api.reply_message(reply_token, message)
    
    return "OK"

def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(original_content_url = url, preview_image_url = url)
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_image_carousel_message(reply_token, labels, texts, image_links):
    line_bot_api = LineBotApi(channel_access_token)
    cols = []
    for i, image_url in enumerate(image_links):
        cols.append(ImageCarouselColumn(image_url=image_url, action=MessageTemplateAction(label=labels[i], text=texts[i])))
    message = TemplateSendMessage(alt_text='ImageCarousel template', template=ImageCarouselTemplate(columns=cols))
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_carousel_message(reply_token, titles, texts, image_links, url_links):
    line_bot_api = LineBotApi(channel_access_token)
    cols = []
    for i, image_url in enumerate(image_links):
        group = CarouselColumn(thumbnail_image_url=image_url, title=titles[i], text=texts[i], actions= [URIAction(label='點我看預告片', uri=url_links[i])] )
        cols.append(group)
    message = TemplateSendMessage(alt_text='Carousel template', template=CarouselTemplate(columns=cols))
    line_bot_api.reply_message(reply_token, message)
    return "OK"