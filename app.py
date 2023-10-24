from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
from mongodb_function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import  os
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('你的Channel AcessToken')
# Channel Secret
handler = WebhookHandler('你的Channel Secret')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    write_one_data(eval(body.replace('false','False')))
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    
    elif '查看我的菜單' in msg:
        user_id = event.source.user_id
        menu_items = get_user_menu(user_id)

        if menu_items:
            menu_text = '\n'.join(menu_items)
            message = TextSendMessage(text=f"你的菜單如下：\n{menu_text}")
        else:
            message = TextSendMessage(text="你還沒有新增任何菜單項目。")

        line_bot_api.reply_message(event.reply_token, message)

    #======MongoDB操作範例======

    elif '@讀取' in msg:
        datas = read_many_datas()
        datas_len = len(datas)
        message = TextSendMessage(text=f'資料數量，一共{datas_len}條')
        line_bot_api.reply_message(event.reply_token, message)

    elif '@查詢' in msg:
        datas = col_find('events')
        message = TextSendMessage(text=str(datas))
        line_bot_api.reply_message(event.reply_token, message)

    elif '@對話紀錄' in msg:
        datas = read_chat_records()
        print(type(datas))
        n = 0
        text_list = []
        for data in datas:
            if '@' in data:
                continue
            else:
                text_list.append(data)
            n+=1
        data_text = '\n'.join(text_list)
        message = TextSendMessage(text=data_text[:5000])
        line_bot_api.reply_message(event.reply_token, message)

    elif '@刪除' in msg:
        text = delete_all_data()
        message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, message)

    #======MongoDB操作範例======

    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

# 處理 Postback 事件
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    user_id = event.source.user_id
    
    if "新增菜單" in data:
        # 解析資料，獲取要新增的菜單項目資訊
        menu_item_data = data.split(":")[1]
        
        # 使用之前提供的函數進行MongoDB操作
        add_menu_item(user_id, menu_item_data)

        # 向使用者發送確認訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{menu_item_data} 已成功新增到菜單。")
        )
    
    elif "刪除菜單" in data:
        # 解析資料，獲取要刪除的菜單項目資訊
        menu_item_data = data.split(":")[1]

        # 使用之前提供的函數進行MongoDB操作
        delete_menu_item(user_id, menu_item_data)
        
        # 向使用者發送確認訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{menu_item_data} 已成功從菜單中刪除。")
        )
    


    

    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
