from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# ใส่ Channel Access Token และ Channel Secret ที่ได้จาก Line Developers Console
line_bot_api = LineBotApi('4wnERCe/5YGKpj4a84afGVt0+yEOn2KIEVlKuyOLL5dmd5GpzqQbXWA6kmJKioWKxZk0sHDw9t4VnL8EMKzZ9K+MNyHr3rMAgYG6+vifVinmNrX+x4J+cCFzBcjHnmatb1bagxC5SFWIIQ3tpPd1wAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3d6dc9f76192a2aee945c45b22ee43f2')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text

    # ตรวจสอบคำสั่งเปิด/ปิดกลุ่ม
    if text.lower() == 'เปิดกลุ่ม':
        reply_text = 'กลุ่มถูกเปิดแล้ว'
        # ทำการเปิดกลุ่ม
        # your_code_to_open_group()
    elif text.lower() == 'ปิดกลุ่ม':
        reply_text = 'กลุ่มถูกปิดแล้ว'
        # ทำการปิดกลุ่ม
        # your_code_to_close_group()
    else:
        
        reply_text = f'คำสั่ง "{text}" ไม่ถูกต้อง'
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


if __name__ == "__main__":
    app.run(debug=True)
    
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text

    if text.startswith('เตะ'):
        user_to_kick = text[3:]  # ข้ามคำว่า 'เตะ' และดึง user_id ที่ต้องการเตะ
        reply_text = f'เตะเพื่อน {user_to_kick} ออกจากกลุ่ม'
        # ทำการเตะเพื่อน
        kick_result = kick_user_from_group(user_to_kick)
        if kick_result:
            reply_text += ' สำเร็จ'
        else:
            reply_text += ' ไม่สำเร็จ'
    elif text.lower() == 'ดึงเพื่อน':
        user_to_invite = event.source.user_id
        reply_text = f'ดึงเพื่อน {user_to_invite} เข้ากลุ่ม'
        # ทำการเชิญเพื่อนเข้ากลุ่ม
        invite_result = invite_user_to_group(user_to_invite)
        if invite_result:
            reply_text += ' สำเร็จ'
        else:
            reply_text += ' ไม่สำเร็จ'
    else:
        reply_text = f'คำสั่ง "{text}" ไม่ถูกต้อง'

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

def kick_user_from_group(user_id):
    try:
        line_bot_api.kickout_from_group(group_id, user_id)
        return True
    except Exception as e:
        print(f'Error kicking user: {e}')
        return False

def invite_user_to_group(user_id):
    try:
        line_bot_api.invite_to_group(group_id, user_id)
        return True
    except Exception as e:
        print(f'Error inviting user: {e}')
        return False

if __name__ == "__main__":
    app.run(debug=True)