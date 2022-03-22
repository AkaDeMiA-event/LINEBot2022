import urllib.request
import json
from .bot_info import access_token

reply_endpoint_url = "https://api.line.me/v2/bot/message/reply"
push_endpoint_url = "https://api.line.me/v2/bot/message/push"
header = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}


class LineMessage:
    def __init__(self, messages):
        # このクラスがインスタンス化された時に実行される。
        self.messages = messages

    def reply(self, reply_token):
        body = {"replyToken": reply_token, "messages": self.messages}
        # print(body)
        # リクエストオブジェクトの作成
        req = urllib.request.Request(
            reply_endpoint_url, json.dumps(body).encode(), header
        )
        try:
            # urllib.request.urlopenでリクエスト送信
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)

    def push(self, user_id):
        body = {"to": user_id, "messages": self.messages}
        req = urllib.request.Request(
            push_endpoint_url, json.dumps(body).encode(), header
        )
        try:
            # urllib.request.urlopenでリクエスト送信
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)


def create_text_message(message):
    test_message = [{"type": "text", "text": message}]
    return test_message
