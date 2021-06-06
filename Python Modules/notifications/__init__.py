import sys
import os
import http.client
import urllib

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

APP_TOKEN = "aktha8d8ank21v4sqakrgxvkivzkkt"
USER_KEY = "u2rd8mbd8q54fmijhfyqksm41d8qjz"

def send(title, message):

    body = {
        "token": APP_TOKEN,
        "user": USER_KEY,
        "message": message,
    }

    if title is not None:
        body["title"] = title

    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode(body),
        {
            "Content-type": "application/x-www-form-urlencoded"
        }
    )
    conn.getresponse()
