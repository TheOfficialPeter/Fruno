import requests
import re
from perplexity import Perplexity

perplexity = Perplexity()

def clean(answer):
    answer = re.sub(r"\[\d+\]", "", answer)
    return answer

def getRecommendedGames(gameName):
    prompt = f"Please show a list of games that are closely similar to the `{gameName}`. ONLY SHOW THE LIST OF NAMES OF THE GAMES"
    promptResponse = perplexity.search(prompt)
    
    answerResponse = ""
    for i in promptResponse:
        answerResponse = i.get('answer')

    answerResponse = clean(answerResponse)
    return answerResponse
