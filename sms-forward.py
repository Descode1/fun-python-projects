from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def receive_sms():
    data = request.json
    sender = data.get("sender")
    message = data.get("message")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] From: {sender}\nMessage: {message}\n")
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
