import requests
from os import makedirs, listdir
from os.path import join, exists

from Constants import *


def get_file(file, path="files/"):
    j_resp = requests.get(TELEGRAM_URL + "getfile", params={"file_id": file["file_id"]}, timeout=5).json()
    if not j_resp["ok"]:
        return 0
    file_path = j_resp['result']["file_path"]
    file_byte = requests.get(FILE_URL + file_path, timeout=5)
    name = (file.get("file_name") if file.get("file_name") is not None else file_path[file_path.index("/") + 1:])
    if name[name.rfind(".") + 1:] not in EXTENSIONS:
        return EXTENSION_ERROR
    if not exists(path):
        makedirs(path)
    name = join(path, name)
    with open(name, "wb") as f:
        f.write(file_byte.content)
    return name


def check_error(chat_id, state, parse_mode="HTML"):
    if not state:
        res = requests.post(TELEGRAM_URL + "sendMessage",
                            json={"chat_id": chat_id, "text": MAIN_ERROR,
                                  "parse_mode": parse_mode,
                                  "disable_web_page_preview": True}).json()
    return state


def send_message(chat_id, text, parse_mode="HTML", markup={}):
    response = requests.post(TELEGRAM_URL + "sendMessage", json={"chat_id": chat_id, "text": text,
                                                                 "parse_mode": parse_mode, "reply_markup": markup,
                                                                 "disable_web_page_preview": True}).json()
    return check_error(chat_id, response["ok"])


def send_photo(chat_id, img_name, text="", parse_mode="HTML", markup={}):
    files = {'photo': open(img_name, 'rb')}
    params = {"chat_id": chat_id, "caption": text, "parse_mode": parse_mode, "reply_markup": markup}
    response = requests.post(TELEGRAM_URL+ "sendPhoto", params=params, files=files).json()
    return check_error(chat_id, response["ok"])


def send_document(chat_id, doc, text="", parse_mode="HTML", markup={}):
    files = {'document': open(doc, 'rb')}
    params = {"chat_id": chat_id, "caption": text, "parse_mode": parse_mode, "reply_markup": markup}
    response = requests.post(TELEGRAM_URL + "sendDocument", params=params, files=files).json()
    return check_error(chat_id, response["ok"])


def make_menu():
    return {"MenuButtonCommands": {"type": "commands"}}


def make_keyboard(buttons, one_time=False, size=(0, 0)):
    if isinstance(buttons, list) or isinstance(buttons, tuple):
        return {"keyboard": [[{"text": t} for t in b] for b in buttons], "resize_keyboard": True,
                "one_time_keyboard": one_time}
    return {"keyboard": [[{"text": t} for t in buttons]], "resize_keyboard": True, "one_time_keyboard": one_time}


##########################HTML functions
