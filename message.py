#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot.models import *

#旋轉木馬按鈕訊息介面

def Carousel_Template():
    message = TemplateSendMessage(
        alt_text='一則旋轉木馬按鈕訊息',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Number_1_in_green_rounded_square.svg/200px-Number_1_in_green_rounded_square.svg.png',
                    title='清蒸鱈魚',
                    text='急速低溫直送鱈魚片，使用一級醬汁及白醋和些許調味料製成。肉質柔軟細嫩',
                    actions=[
                        PostbackTemplateAction(
                            label='加入菜單',
                            data='新增菜單:清蒸鱈魚'
                        ),
                        # PostbackTemplateAction(
                        #     label='移出菜單',
                        #     data='刪除菜單:清蒸鱈魚'
                        # )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Number_1_in_green_rounded_square.svg/200px-Number_1_in_green_rounded_square.svg.png',
                    title='清蒸鱈魚2',
                    text='急速低溫直送鱈魚片，使用一級醬汁及白醋和些許調味料製成。肉質柔軟細嫩',
                    actions=[
                        PostbackTemplateAction(
                            label='加入菜單',
                            data='新增菜單:清蒸鱈魚2'
                        ),
                        # PostbackTemplateAction(
                        #     label='移出菜單',
                        #     data='刪除菜單:清蒸鱈魚2'
                        # )
                    ]
                )
            ]
        )
    )
    return message


#關於LINEBOT聊天內容範例
