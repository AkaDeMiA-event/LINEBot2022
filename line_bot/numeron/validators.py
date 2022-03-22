from django.http import HttpResponse
from .request_create import LineMessage, create_text_message


def can_convert_to_int(message_text):
    try:
        # 文字列を実際にint関数で変換してみる
        int(message_text, 10)
    except ValueError:
        # 例外が発生＝変換できないのでFalseを返す
        return False
    else:
        # 変換できたのでTrueを返す
        return True


def is_overlapping(num_array):
    return len(num_array) != len(set(num_array))


# line_botからの入力をvalidateしてOKなら配列を返す関数を定義　単体テストずみ
def validate_or_process_message(message_text):
    # 数字に変換可能か。
    if can_convert_to_int(message_text):
        number = int(message_text)
        if number > 0:
            # numberは正の整数 message_textは数値変換可能なもの
            if len(message_text) == 4:
                list_str = list(message_text)
                # 1文字ずつに分離して数字に
                list_num = [int(s) for s in list_str]
                if not is_overlapping(list_num):
                    return list_num

    return False
