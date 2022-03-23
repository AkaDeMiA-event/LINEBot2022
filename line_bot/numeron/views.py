from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
import random
import json
import base64
import hashlib
import hmac
from .models import Numeron
from .request_create import LineMessage, create_text_message
from .validators import validate_or_process_message
from .bot_info import channel_secret
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.views import LoginView

# djangoのpostはcsrf_tokenを必要としているがLINEのpostリクエストではcsrfできない。→csrfの例外として設定。
@csrf_exempt
def index(request):
    if request.method == "POST":
        # Request body string
        body = request.body.decode("utf-8")
        hash = hmac.new(
            channel_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
        ).digest()
        signature = base64.b64encode(hash)
        try:
            assert (
                request.META.get("HTTP_X_LINE_SIGNATURE").encode("utf-8") == signature
            )
        except:
            return HttpResponseBadRequest("badrequest")
        # lineのエンドポイントにおくるリクエストに必要なもの定義
        request = json.loads(request.body.decode("utf-8"))
        events = request["events"]
        if not events:
            return HttpResponse("Developers verify")
        data = events[0]
        message = data["message"]
        reply_token = data["replyToken"]
        user_id = data["source"]["userId"]

        # スタンプやメディア系をバリデーション
        if message["type"] == "text":
            message_text = message["text"]
        else:
            line_message = LineMessage(create_text_message("不正な入力です。"))
            line_message.reply(reply_token)
            return HttpResponse("スタンプやメディア系をバリデーション")

        all_data = Numeron.objects.filter(line_id=user_id)
        if message_text == "start":
            # データベースに一つの値だけにしたい。

            if all_data.exists():
                all_data.delete()
                line_message = LineMessage(
                    create_text_message("ゲームがリスタートしました。4桁の数字を入力してください。")
                )
            else:
                line_message = LineMessage(
                    create_text_message("ゲームがスタートしました。4桁の数字を入力してください。")
                )

            # ランダムに数字を生成 重複なしの４つの数字
            random_number_array = random.sample(range(0, 10), k=4)
            target_num_str = "".join(map(str, random_number_array))
            Numeron.objects.create(number_str=target_num_str, line_id=user_id)

            line_message.reply(reply_token)
            return HttpResponse("ゲームスタート")

        elif message_text == "stop":
            if all_data.exists():
                all_data.delete()
                line_message = LineMessage(create_text_message("ゲームが終了しました。"))
                line_message.reply(reply_token)
                return HttpResponse("ゲーム終了")
            line_message = LineMessage(create_text_message("ゲームが始まっていません。"))
            line_message.reply(reply_token)
            return HttpResponse("スタートしてないゲームは終了できない")

        elif all_data.exists():
            # number_dataにはFalseか数字の配列が格納される。
            # validate_or_process_messageは入力された値をバリデーションし、正しい入力の場合数値の配列を返す。
            number_data = validate_or_process_message(message_text)
            if number_data:
                # number_dataが正しく定義されていた場合に動く
                # numeron本体の処理
                try:
                    target_str = Numeron.objects.get(line_id=user_id).number_str
                except:
                    line_message = LineMessage(create_text_message("データベースに異常があります。"))
                    line_message.reply(reply_token)
                    return HttpResponse("データベースに値が想定外の入り方してる。")
                # 比較対象の配列
                target = [int(x) for x in list(target_str)]
                # ただしく動いている
                # この部分を書かせたい。
                eat = 0
                bite = 0
                for number in number_data:
                    index = number_data.index(number)
                    if number in target:
                        if number == target[index]:
                            eat += 1
                        else:
                            bite += 1
                reply_message = f"{eat}EAT-{bite}BITE"
                if eat == 4:
                    reply_message += "\nゲームクリア！！！\nおめでとう！！！"
                    all_data.delete()
                line_message = LineMessage(create_text_message(reply_message))
                line_message.reply(reply_token)
                return HttpResponse("ゲームの正常形")

            else:
                line_message = LineMessage(create_text_message("不正な入力です。"))
                line_message.reply(reply_token)
                return HttpResponse("数字の異常形をバリデーション")
        else:
            line_message = LineMessage(
                create_text_message("不正な入力です。ゲームを始める場合はstartと入力してください。")
            )
            line_message.reply(reply_token)
            return HttpResponse("数字の異常形をバリデーション")


# LINEの返信の基本形を示す。
@csrf_exempt
def reply(request):
    if request.method == "POST":
        # Request body string
        body = request.body.decode("utf-8")
        hash = hmac.new(
            channel_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
        ).digest()
        signature = base64.b64encode(hash)
        try:
            assert (
                request.META.get("HTTP_X_LINE_SIGNATURE").encode("utf-8") == signature
            )
        except:
            return HttpResponseBadRequest("badrequest")
        # lineのエンドポイントにおくるリクエストに必要なもの定義
        request = json.loads(request.body.decode("utf-8"))
        events = request["events"]
        if not events:
            return HttpResponse("Developers verify")
        data = events[0]
        message = data["message"]
        reply_token = data["replyToken"]
        user_id = data["source"]["userId"]

        # スタンプやメディア系をバリデーション
        if message["type"] == "text":
            message_text = message["text"]
        else:
            line_message = LineMessage(create_text_message("不正な入力です。"))
            line_message.reply(reply_token)
            return HttpResponse("スタンプやメディア系をバリデーション")

        # おうむ返しのコード
        # message_textの部分をいじれば好きな文言に変えることができる。
        line_message = LineMessage(create_text_message(message_text))
        line_message.reply(reply_token)
        return HttpResponse("おうむ返し")
