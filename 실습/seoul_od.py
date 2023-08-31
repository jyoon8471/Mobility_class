# 모듈 불러오기
import requests, json
import pandas as pd
import numpy as np

# 서울시 지역정보 csv 파일 불러오기
seoul_areacode = pd.read_csv('seoul_sgg_emd.csv', encoding='utf-8-sig')

# 읍면동 코드만 따로 불러오기
emdCd = seoul_areacode['emdCd']

key = "20230816155829gpibn3h2c46t4jt5t30vp4iu7c"
date = "20210630"
url_base = "https://stcis.go.kr/openapi/quarterod.json?apikey={}&opratDate={}&stgEmdCd={}&arrEmdCd={}"



# od matrix 뼈대 만들기
od = np.zeros((len(emdCd), len(emdCd)))

# API를 통해 각 od-pair별 이동량 불러오고, od matrix에 넣어주기
for i in range(len(emdCd)):
    for j in range(len(emdCd)):
        org = emdCd[i]
        dest = emdCd[j]
        
        url = url_base.format(key, date, org, dest)

        resp = requests.get(url)
        data = resp.json()['result'][0]
        
        flow = data['useStf'] * 4  # flow rate
        
        od[i, j] = flow
        
        




