from tkinter import SE
from requests import post, Session
from fake_useragent import UserAgent
from lxml import html
import pandas as pd
import config



# Ссылки на страницы:
link = "https://passport.yandex.ru/auth/" # Адрес для логирования
link_mail = "https://mail.yandex.ru/lite/unread" #Адрес непрочитанной почты в версии лайт

user = UserAgent().random

HEADER = {
'user-agent': user
}

# Логин и пароль из файла конфиг
data = {
'login': config.user_name,
'passwd': config.user_password,
}

class SearchMail():

    def __init__(self, link, link_mail, data):
        self.link = link
        self.link_mail = link_mail
        self.data = data

    def get_text(self):
        # Создаем сессию
        session = Session()
        response = session.post(self.link, headers=HEADER, data=self.data) # входим на сайт и записываем ответ
        response_mail = session.get(self.link_mail, headers=HEADER) # получаем данные с сайта почты
        dom = html.fromstring(response_mail.text)
        return dom


    def xpath_info(self):
        dom = self.get_text()

        # Ищем данные на сайте при помощи xpath для заполнения таблицы
        mail_from = dom.xpath('//span[contains(@class, "b-messages__from__text")]/span/text()') # Имя отправителя
        mail_subject = dom.xpath('//span[contains(@class, "b-messages__subject")]/span/text()') # Тема письма
        mail_time = dom.xpath('//span[contains(@class, "b-messages__date")]/span/text()') # Время письма
        mail_link = dom.xpath('//a[contains(@class, "b-messages__message__link")]/@href') # Ссылка на письмо
        
        mail_box = [] # Список писем
        
        for i in range(len(mail_from)):

            data = {}
            data['From'] = mail_from[i]
            data['Subject'] = mail_subject[i]
            data['Time'] = mail_time[i]
            data['Link'] = self.link_mail + mail_link[i]

            mail_box.append(data)
    
        return mail_box


# Тестируем работу
parse_mail = SearchMail(link, link_mail, data)
# response, response_mail = parse_mail.get_text()
# with open("response.html", "w") as file:
#     file.write(response)

# with open("response_mail.html", "w") as file:
#     file.write(response_mail)

mail_box = pd.DataFrame(parse_mail.xpath_info())
print(mail_box)

# К сожалению, очень много времени потрачено на попытки обойти проверки подлинности от Яндекса. К сожалению, действенного способа не найдено, кроме как
# просто не ставить проверки в принципе.