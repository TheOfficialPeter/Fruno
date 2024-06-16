import google.generativeai as genai
from config import GEMINI_TOKEN

genai.configure(api_key=GEMINI_TOKEN)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

def getRecommendedGames(gameName):
    # Create new chat session
    chat_session = model.start_chat()
    
    prompt = f"Please show a list of games that are closely similar to the `{gameName}`. ONLY SHOW THE LIST OF NAMES OF THE GAMES"
    response = chat_session.send_message(prompt)
    
    return response.text
