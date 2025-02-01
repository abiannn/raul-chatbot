from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = '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'

class Chatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)
    
    def get_response(self, user_input):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": user_input}],
                model="mixtral-8x7b-32768",
            )
            response = chat_completion.choices[0].message.content
            return response
        except Exception as e:
            print(f"Kesalahan saat menghasilkan respons dari API Groq: {e}")
            return "Kesalahan: Tidak dapat memproses permintaan"

chatbot = Chatbot(api_key=GROQ_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        if not user_message:
            raise ValueError("Pesan tidak diterima")
        print(f"Pesan yang diterima: {user_message}")
        bot_response = chatbot.get_response(user_message)
        return jsonify({'message': bot_response})
    except Exception as e:
        print(f"Kesalahan: {e}")
        return jsonify({'message': 'Kesalahan: Tidak dapat memproses permintaan Anda'}), 500

if __name__ == '__main__':
    app.run(debug=True)
