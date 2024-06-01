import os
from openai import OpenAI 
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    content_type = request.headers.get('Content-Type', '')
    
    if content_type == 'application/json':
        data = request.json
    else:
        data = request.form
    
    
    question = data.get('question', [])

    responses = []
    for q in question:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": f"{q}"},
                {"role": "assistant", "content": "As a Cisco-focused assistant, I can help you with queries related to network configurations, Cisco products, troubleshooting, and more."}
            ]
        )

        result = ''
        for choice in response.choices:
            result += choice.message.content
        
        responses.append(result)
    return jsonify({"responses": responses})

if __name__ == '__main__':
    app.run(debug=True)
