import requests
import json

api_response = requests.get('https://dummyjson.com/products')
# print(api_response.status_code)
data = api_response.text
parse_json = json.loads(data)
print(parse_json)