import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://forum.netmarble.com/enn_ko/list/33/"

r = requests.get(URL)
soup = BeautifulSoup(r.text, "html.parser")

title = soup.select_one("tbody tr td a")

latest_title = title.text.strip()
latest_link = "https://forum.netmarble.com" + title["href"]

old_title = ""

if os.path.exists("last.txt"):
    with open("last.txt","r",encoding="utf-8") as f:
        old_title = f.read().strip()

if latest_title != old_title:

    token = os.environ["KAKAO_TOKEN"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": f"새 공지 등록\n{latest_title}\n{latest_link}",
            "link": {
                "web_url": latest_link
            }
        })
    }

    requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers=headers,
        data=data
    )

    with open("last.txt","w",encoding="utf-8") as f:
        f.write(latest_title)
