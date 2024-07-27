import aiohttp
import asyncio
import json

async def fetch_data():
    url = "https://isthereanydeal.com/api/game/info/"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.6",
        "content-type": "application/json",
        "itad-sessiontoken": "LwsZZEBvwuOeq3tsgq9LEb8E09UL9x4oTKOa92Mu0mMheXMK",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Brave\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "cookie": "PHPSESSID=pijnfkvm9lufu9c5qds7vnq911; country=ZA; visitor=669bf0bd82ff99.11909582; session_id=0190d124-7bbc-71ba-a1f7-92b992a40f06",
        "Referer": "https://isthereanydeal.com/game/astroneer/info/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    data = {"gid": "018d937e-f969-72ed-a245-152daff6edb7"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            json_data = await response.json()
            print(json_data)

# Run the coroutine
asyncio.run(fetch_data())