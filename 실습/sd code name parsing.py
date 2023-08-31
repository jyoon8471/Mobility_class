
# requests 모듈을 통해 API 데이터 받아오고, json 형태로 저장하기
import requests, json

key = "20230816155829gpibn3h2c46t4jt5t30vp4iu7c"
url = "https://stcis.go.kr/openapi/areacode.json?apikey={}&sdCd=&sggCd=".format(key)

resp = requests.get(url)
data = resp.json()['result']




# 반복문을 이용하여 json 데이터를 파싱하고 dataframe 형태로 만들기
import pandas as pd

attributes = list(data[0].keys())
data_frame = []
for i in range(len(data)):
    tmp_data = data[i]
    tmp_value = []
    for j in range(len(attributes)):
        tmp_value.append(data[i][attributes[j]])
    
    data_frame.append(tmp_value)

df = pd.DataFrame(data_frame)
df.columns = attributes



# to_csv를 이용하여 dataframe을 csv파일로 저장하기
df_csv = df[['sdCd', 'sdNm']]
df_csv.to_csv("sd_code-name.csv", index = False)

# enconding 방식을 utf-8-sig 로 지정하여 저장하기
df_csv.to_csv("sd_code-name.csv", index = False, encoding='utf-8-sig')




