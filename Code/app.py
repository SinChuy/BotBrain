from flask import Flask, jsonify, request
from twitch_bot import TwitchBot

app = Flask(__name__)
bot = TwitchBot()

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    bot.send_message(message)
    return jsonify({'success': 'Message sent'})

if __name__ == '__main__':
    app.run(debug=True)
