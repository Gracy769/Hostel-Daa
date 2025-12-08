import openai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = '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'

# Memory to hold conversation history (optional, but makes the bot more dynamic)
conversation_history = []

# Function to generate response from GPT-3 (or GPT-4)
def generate_response(user_message):
    # Add the user message to the conversation history for context
    conversation_history.append({"role": "user", "content": user_message})
    
    # Get response from OpenAI's GPT-3 (or GPT-4)
    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can use gpt-3.5-turbo or any available model
        messages=conversation_history,
        max_tokens=150,  # Limit response length
        temperature=0.9,  # Make responses more creative
    )

    # Extract the text response from the model
    bot_response = response['choices'][0]['message']['content']
    
    # Add bot response to conversation history
    conversation_history.append({"role": "assistant", "content": bot_response})
    
    return bot_response

# Define API endpoint to interact with the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Generate response based on user input
    bot_output = generate_response(user_input)
    
    return jsonify({"response": bot_output})

if __name__ == '__main__':
    app.run(debug=True)
