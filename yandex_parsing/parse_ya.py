from requests import post, Session
from fake_useragent import UserAgent
from lxml import html
import pandas as pd
import config



# # Ссылки на страницы:
# link = "https://passport.yandex.ru/auth/" # Адрес для логирования
# link_mail = "https://mail.yandex.ru/lite/unread" # Адрес непрочитанной почты в версии лайт
# link_draft = "https://mail.yandex.ru/lite/draft" # Адрес черновиков

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

    
    
    
    def __init__(self, data):
        # self.link = link
        # self.link_mail = link_mail
        self.data = data
        # Ссылки на страницы:
        self.link = "https://passport.yandex.ru/auth/" # Адрес для логирования
        self.link_unread = "https://mail.yandex.ru/lite/unread" # Адрес непрочитанной почты в версии лайт
        self.link_draft = "https://mail.yandex.ru/lite/draft" # Адрес черновиков
        self.link_mail = "https://mail.yandex.ru"
        self.send_button = "https://mail.yandex.ru/lite/compose-action.xml"

        self.session = Session()

    def get_text(self):
        # Создаем сессию
        response = self.session.post(self.link, headers=HEADER, data=self.data) # входим на сайт и записываем ответ
        response_unread = self.session.get(self.link_unread, headers=HEADER) # получаем данные с сайта почты
        response_draft = self.session.get(self.link_draft, headers=HEADER)
        
        return html.fromstring(response_unread.text), html.fromstring(response_draft.text)


    def get_unread(self):
        dom, _ = self.get_text()

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
    
    def send_mail(self):
        _, dom = self.get_text()
        mail_subject = dom.xpath('//span[contains(@class, "b-messages__subject")]/span/text()') # Тема письма
        mail_link = dom.xpath('//a[contains(@class, "b-messages__message__link")]/@href') # Ссылка на письмо
        mail_box = [] # Список писем
        for i in range(len(mail_link)):

            data = {}
            data['Subject'] = mail_subject[i]
            data['Link'] = self.link_mail + mail_link[i]

            mail_box.append(data)
        
        for i in mail_box:
            response_draft = self.session.get(i['Link'], headers=HEADER)
            # send_button = html.fromstring(response_draft).xpath('//input[contains(@class, "b-compose__send")]')
            response_send = self.session.post(self.send_button, headers=HEADER)
            print(response_send)
        
        return mail_box

            
        
        



# Тестируем работу
parse_mail = SearchMail(data)
# response, response_mail = parse_mail.get_text()
# with open("response.html", "w") as file:
#     file.write(response)

# with open("response_mail.html", "w") as file:
#     file.write(response_mail)

mail_box = pd.DataFrame(parse_mail.get_unread())
draft_mail = pd.DataFrame(parse_mail.send_mail())
print(mail_box)
print(draft_mail)

# К сожалению, очень много времени потрачено на попытки обойти проверки подлинности от Яндекса. К сожалению, действенного способа не найдено, кроме как
# просто не ставить проверки в принципе. Это касается именно способов прохождения проверки при помощи requests. 