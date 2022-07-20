from requests import post, Session
from fake_useragent import UserAgent
import pandas as pd
import config

link = "https://passport.yandex.ru/auth/"
link_mail = "https://mail.yandex.ru/lite/unread/"
user = UserAgent().random

HEADER = {
'user-agent': user
}

data = {
'login': config.user_name,
'passwd': config.user_password,
}

session = Session()

session.post(link, headers=HEADER, data=data)
response_mail = session.get(link_mail, headers=HEADER)

# with open("response.html", "w") as file:
#     file.write(response.text)

with open("response_mail.html", "w") as file:
    file.write(response_mail.text)

 