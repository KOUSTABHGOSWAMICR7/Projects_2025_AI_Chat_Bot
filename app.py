from flask import Flask, render_template, request, jsonify
from main import ChatbotAssistant, get_stocks

app = Flask(__name__)

assistant = ChatbotAssistant("intents.json", function_mappings={"stocks": get_stocks})
assistant.parse_intents()
assistant.load_model("chatbot_model.pth", "dimensions.json")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['message']
    response = assistant.process_message(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)