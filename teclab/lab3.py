import requests
import json
import csv

response = requests.post('___', json={"username": "test",
    "password": "MX3xMQ8P"})
token = (response.json()['token'])

params = {
    "offset": 0,
    "limit": 50
}
headers = {"Authorization": f"Bearer {token}"}
response = requests.get('___', params=params, headers=headers)

if response.ok:
    data = json.loads(response.text)


data_file = open('response_headers.csv', 'w', encoding='utf8', newline='')
csv_writer = csv.writer(data_file)

count = 0
dict_filter = lambda x, y: dict([(i,x[i]) for i in x if i in set(y)])
dict_keys = ('id', 'displayName')

for d in data:
    small_dict = dict_filter(d, dict_keys)

    if count == 0:
        header = small_dict.keys()
        csv_writer.writerow(header)
        count += 1
    for i in small_dict:
        small_dict[i] = small_dict[i].strip('\t')

    csv_writer.writerow(small_dict.values())
    print(small_dict.values())

data_file.close()