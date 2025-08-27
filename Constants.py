from MessageStylist import *

BOT_TOKEN = ""
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
FILE_URL = f"https://api.telegram.org/file/bot{BOT_TOKEN}/"
USER_URL = "tg://user?id="

DB_NAME = "Users_data.db"
USERS_TABLE = "Users"

MODEL_LIB = 'NVIDIA/DeepLearningExamples:torchhub'
PRETRAIND_MODEL = 'nvidia_efficientnet_b4'
MODEL_PATH = ""
MODEL_NAME = "Efficientnet_b4_model_8_20230507_181213"
THRESHOLD = 0.8

COMMANDS = {'/info': "info",
            }

COMMUTATOR = {
            0: "handleFile",
            }

EXTENSIONS = ["jpg", "jpeg", "png"]

LABELS = ["Normal", "Tuberculosis", "Pneumonia", "COVID19"]

MAIN_ERROR = "Something went wrong... Please try again"
EXTENSION_ERROR = f"File have to be in one of these extensions: {', '.join([b(ext) for ext in EXTENSIONS])}"
HELLO_PHRASE = "Hello!"
BOT_INFO = f"I am a bot that detects the presence of lung diseases by X-ray, such as {b('tuberculosis, pneumonia and covid19')}. I am always ready to help you!!!"
BACK_MSG = "You are in the main menu"
SENDME_MSG = f"Send me your file (it have to in one of these extensions: {', '.join([b(ext) for ext in EXTENSIONS])})"
OUT_OF_FILE = "The file was not found. Please try again"
pre_s = '\n'.join([b('{} - {:.1%}') for _ in range(len(LABELS[1:]))])
VERDICT = f"The probability you are sick is:\n{pre_s}."
VERDICTS = [f"I think you are {b('OK')}!",
            f"Probably you are {b('SICK')}. I think you should get checked out by a doctor!",
            f"Probably you are {b('SICK')}: {b('{}')}. I think you should get checked out by a doctor!"]