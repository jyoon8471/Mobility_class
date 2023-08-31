import requests, json

base_url = "https://stcis.go.kr/openapi/"
functions = ["areacode", "busroute", "busroutesttn", "bussttn", "quarterod"]
key = "20230816155829gpibn3h2c46t4jt5t30vp4iu7c"

url = "https://stcis.go.kr/openapi/areacode.json?apikey={}&sdCd=&sggCd=".format(key)

resp = requests.get(url)
data = resp.json()


parsed_data = json.loads(data)






ex = '{"a" : "apple", "b" : "banana"}'
dic = json.loads(ex)
