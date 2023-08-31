
# 서울시 sggCd와 sggNm을 데이터프레임으로 만들고 csv 파일로 저장하기
import requests, json
import pandas as pd

key = "20230816155829gpibn3h2c46t4jt5t30vp4iu7c"
url = "https://stcis.go.kr/openapi/areacode.json?apikey={}&sdCd={}&sggCd={}".format(key, 11, '')

resp = requests.get(url)
data = resp.json()['result']


# 반복문을 이용하여 json 데이터를 파싱하고 dataframe 형태로 만들기
attributes = list(data[0].keys())
data_frame = []
for i in range(len(data)):

    tmp_value = []
    
    for j in range(len(attributes)):
        tmp_value.append(data[i][attributes[j]])
    
    data_frame.append(tmp_value)

df = pd.DataFrame(data_frame)
df.columns = attributes


# 비어있는 열 제거
attributes_valid = df.columns[df.notna().any()].tolist()
df_csv = df[attributes_valid]
df_csv.to_csv("seoul_sgg.csv", index = False, encoding='utf-8-sig')





# 각 구별 읍면동 정보 가져오기
data_frame_emd = []
total_data_length = 0

for sgg in df_csv['sggCd']:
    
    url_sgg = "https://stcis.go.kr/openapi/areacode.json?apikey={}&sdCd={}&sggCd={}".format(key, 11, sgg)
    
    resp = requests.get(url_sgg)
    data_len = resp.json()['count']
    data = resp.json()['result']
    total_data_length += data_len
    
    if data_len != len(data):
        print("error")
        break
    
    for i in range(data_len):
        tmp_value_emd = []
        
        for j in range(len(attributes)):
            tmp_value_emd.append(data[i][attributes[j]])
            
        data_frame_emd.append(tmp_value_emd)

if total_data_length != len(data_frame_emd):
    print("error")

df_emd = pd.DataFrame(data_frame_emd)
df_emd.columns = attributes

# 비어있는 열 제거
attributes_valid = df_emd.columns[df_emd.notna().any()].tolist()
df_emd_csv = df_emd[attributes_valid]
df_emd_csv.to_csv("seoul_sgg_emd.csv", index = False, encoding='utf-8-sig')





