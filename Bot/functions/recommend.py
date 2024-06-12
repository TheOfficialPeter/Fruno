import requests
import re
from perplexity import Perplexity

perplexity = Perplexity()

def clean(answer):
    answer = re.sub(r"\[\d+\]", "", answer)
    return answer

def getRecommendedGames(gameName):
    placeholder = "Please show a list of games that are closely similar to the one listed below. ONLY SHOW THE NAME OF THE GAMES"
    prompt = placeholder + {gameName}
    
    answer = perplexity.search(prompt)
    
    final = ""
    for a in answer:
        final = a.get('answer')

    final = clean(final)
    return final
