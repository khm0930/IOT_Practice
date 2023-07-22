import requests
import json

api_key = "jnTHgKSIZ51No9LSrrs1Jgrr6zQc62mgTQnU%2Bi%2BFFABtAsCTvKyXafzaolU9CBSjIeiqyoLhgeIXQgbGxrBUoQ%3D%3D"
api_key_decode = requests.utils.unquote(api_key)

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = {
    'serviceKey': api_key_decode,
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'JSON',
    'base_date': '20230722',
    'base_time': '0600',
    'nx': '55',
    'ny': '127'
}

response = requests.get(url, params=params)
r_dict = json.loads(response.text)
r_response = r_dict.get("response")
r_body = r_response.get("body")
r_items = r_body.get("items")
r_item = r_items.get("item")

result = {}
for item in r_item:
    if item.get("category") == "T1H":
        result = item
        break

print(result)
