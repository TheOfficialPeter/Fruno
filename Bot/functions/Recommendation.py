import requests
import re
from ai.perplexity import Perplexity

perplexity = Perplexity()

def clean(answer):
    answer = re.sub(r"\[\d+\]", "", answer)
    return answer

def getRecommendedGames(gameName):
    prompt = f"Games like {gameName}"
    answer = perplexity.search(prompt)
    final = ""
    for a in answer:
        final = a.get('answer')

    final = clean(final)