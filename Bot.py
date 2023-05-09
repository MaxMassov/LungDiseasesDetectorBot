from datetime import datetime as dt
import time
from os import remove
import numpy as np

from TelegramUtils import *
from DatabaseWorker import set_connection
from Model import LungsModel

def start_bot(request):
    try:

        if not request.get("ok") in [None, True]:
            with open("Request.txt", "a+") as file:
                file.write(f"{dt.now()} Request: {request}\n")
            return 0

        if len(request["result"]) == 0 or (request["result"][-1].get("message") is None
                                           and request["result"][-1].get("callback_query") is None):
            return 0

        if request["result"][-1].get("message") is None:
            return 0

        path = request["result"][-1]
        chat_id = path['message']["chat"]["id"]

        if path["message"]["from"]["is_bot"]:
            send_message(chat_id, "Я не общаюсь с другими ботами")
            return 1

        if path['message'].get("text") is not None:
            text = path["message"]["text"].lower().strip()
            file = {}
        elif path['message'].get("document") is not None:
            file = path['message'].get("document")
            text = ""#(path['message'].get("caption") if path['message'].get("caption") is not None else "")
        elif path['message'].get("photo") is not None:
            file = path['message']["photo"][-1]
            text = ""#(path['message'].get("caption") if path['message'].get("caption") is not None else "")
        else:
            return send_message(chat_id, MAIN_ERROR, markup=MAIN_KEYBOARD)

        if text == "/start":
            res = set_connection("insert", chat_id, query_type="-")
            return info(chat_id, start=1)

        res = set_connection("select_session", chat_id)

        if text in ["/menu", "menu"]:
            return menu(chat_id)

        if text in ["/info", "info"]:
            return info(chat_id)

        if not isinstance(res, tuple):
            return send_message(chat_id, MAIN_ERROR, markup=MAIN_KEYBOARD)

        session, query_type = res

        if len(text) > 0 and "/" + text.split(" ")[0] in COMMANDS.keys():
            return globals()[COMMANDS["/" + text.split(" ")[0]]](chat_id, file=file, text=(text.split(" ")[1:] if len(text.split(" ")) > 1 else ""),
                                                                 session=0, query_type="/" + text.split(" ")[0])

        return globals()[COMMUTATOR[session]](chat_id, file=file, text=text, session=session, query_type=query_type)

        '''
        USER:
            id
            is_bot
            first_name
            last_name
            username
            language_code

        MESSAGE:
            text
            entities
            animation
            audio
            document
            photo
            sticker
            video
            video_note
            voice
            caption
            caption_entities
        '''

    except Exception as ex:
        print(f"Error: {ex}")
        with open("Error.txt", "a+") as file:
            file.write(f"{dt.now()} Error: {ex}\n")
        return 0


def info(chat_id, start=0):
    set_connection("update", chat_id, session=0, query_type="-")
    return send_message(chat_id, (HELLO_PHRASE + " " if start else "") + BOT_INFO,
                        markup=MAIN_KEYBOARD)


def menu(chat_id):
    res = set_connection("update", chat_id, session=0, query_type="-")
    send_message(chat_id, BACK_MSG,
                    markup=MAIN_KEYBOARD)
    return True

def newQuery(chat_id, **kwargs):
    kwargs["query_type"] = kwargs.get("text")
    if check_query_type(kwargs):
        send_message(chat_id, MAIN_ERROR)
        return 0
    set_connection("update", chat_id, session=1, query_type=kwargs.get("query_type"))
    send_message(chat_id, SENDME_MSG, markup=MENU_KEYBOARD)
    return 1


def handleFile(chat_id, **kwargs):
    if kwargs.get("session") is None:
        send_message(chat_id, MAIN_ERROR, markup=MENU_KEYBOARD)
        return 0
    if kwargs.get("file") is None or kwargs.get("file") == {}:
        send_message(chat_id, OUT_OF_FILE, markup=MENU_KEYBOARD)
        return 1
    file = get_file(kwargs.get("file"))
    if file == EXTENSION_ERROR:
        send_message(chat_id, EXTENSION_ERROR, markup=MENU_KEYBOARD)
        remove(file)
        return 1
    if file == 0:
        send_message(chat_id, MAIN_ERROR, markup=MENU_KEYBOARD)
        remove(file)
        return 0
    if isinstance(set_connection("update", chat_id, session=0, query_type="-"), str):
        send_message(chat_id, MAIN_ERROR, markup=MENU_KEYBOARD)
        remove(file)
        return 0
    prediction = MODEL.forward(file)
    remove(file)
    pairs = list(zip(LABELS[1:], prediction[1:]))
    verd_sort = []
    for l, p in sorted(pairs, key=lambda x: -x[1]):
        verd_sort.append(l)
        verd_sort.append(p)
    verd = ""
    if np.argmax(prediction) == 0 and prediction[0] > THRESHOLD:
        verd = VERDICTS[0]
    elif np.argmax(prediction) == 0:
        verd = VERDICTS[1]
    else:
        verd = VERDICTS[2].format(LABELS[np.argmax(prediction)])
    send_message(chat_id, VERDICT.format(*verd_sort) + "\n" + verd, markup=MAIN_KEYBOARD)
    return 1

################################

def check_session(kwargs):
    return kwargs.get("session") is None or kwargs.get("session") == 0

def check_query_type(kwargs):
    return kwargs.get("query_type") is None or not (kwargs.get('query_type') in COMMANDS.keys())

######################################

def check_updates(timeout=3):
    old = {}
    while True:
        res = requests.post(TELEGRAM_URL + "getUpdates", data={"limit": 1, "offset": -1}).json()

        if old != res["result"]:
            print(res)
            old = res["result"]
            print(start_bot(res))
        time.sleep(timeout)


######################################

MAIN_KEYBOARD = make_keyboard(COMMANDS.keys())
MENU_KEYBOARD = make_keyboard([["/menu"]])
MODEL = LungsModel()

if __name__ == "__main__":
    check_updates()

