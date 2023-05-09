from flask import Flask, request, json, Response
from Bot import start_bot

app = Flask(__name__)


@app.route('/', methods=["POST", 'GET'])
def index():
    if request.method == 'POST':
        message = json.loads(request.data)
        print(message)
        print(start_bot(message))
        return Response("Ok", status=200)
    else:
        return 'Hello World!'


if __name__ == '__main__':
    app.run()