import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


### step 1 : 데이터 불러오기
import pandas as pd

df = pd.read_csv('지하철_역별OD_20230731.csv', encoding='CP949')

### step 2 : 필요한 컬럼만 선택하기
df = df[['승차_호선', '승차_역', '하차_호선', '하차_역', '총_승객수']]


#######################################################################################################
#######################################################################################################
#######################################################################################################


# Exercise 1: 가장 혼잡한 정류장 top 10은?
#-- ver 1 : Easy but messy
stations = df['승차_역'].unique()

station_nb = []
for i in range(len(stations)):
    station = stations[i]
    
    board = df[df['승차_역'] == station]['총_승객수'].sum()
    alight = df[df['하차_역'] == station]['총_승객수'].sum()
    
    station_nb.append([station, board + alight])

station_nb = pd.DataFrame(station_nb)
station_nb.columns = ['station', 'total_pax']

top10 = station_nb.sort_values(by='total_pax', ascending = False)[:10]
top10 = top10.reset_index(drop = True)



#-- ver 2 : simple version

# Exercise 1: 가장 혼잡한 정류장 top 10은?

### step 1 : 각 역별 총 이용자수 계산하기
boarding_counts = df.groupby('승차_역')['총_승객수'].sum()
alighting_counts = df.groupby('하차_역')['총_승객수'].sum()
total_counts = boarding_counts.add(alighting_counts, fill_value = 0)

### step 2 : 역 이용자수에 따라 내림차순으로 정렬하기
top10 = total_counts.sort_values(ascending = False).head(10)

top10 = pd.DataFrame({
    'station' : top10.index,
    'pax' : top10.values})

### step 3 : 막대그래프 그리기
plt.figure(figsize=(10, 6))
plt.bar(top10['station'], top10['pax'], color='blue')
plt.xlabel('역명')
plt.ylabel('총 이용자수')
plt.title('Top 10 역별 총 이용자수')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig('top10_bar_chart.png')
plt.show()






#######################################################################################################
#######################################################################################################
#######################################################################################################



# Exercise 2 : Folium 모듈을 사용해 top10 정류장을 지도에 표시하기

### step 1 : 지하철역명을 key, 위경도좌표가 value인 dictionary 만들기
coord = pd.read_csv('station_coordination.csv', encoding='CP949')

station_coord_dict = {}
for key, x_coord, y_coord in zip(coord['역사명'], coord['위도'], coord['경도']):
    station_coord_dict[key] = [x_coord, y_coord]

### step 2 : 기본 지도 만들기
import folium

center = [37.51883, 126.9894]
map = folium.Map(location = center, zoom_start = 12)

### step 3 : 지도에 circle marker 추가하기
for i in range(len(top10)):
    station = top10['station'][i]
    folium.CircleMarker(location = station_coord_dict[station], 
                        radius = top10['pax'][i] / 5000,
                        popup = (top10['station'][i] + str(i+1), '위'),
                        color = '#3186cc',
                        fill_color = '#3186cc').add_to(map)

map.save('./map_with_circles.html')

#######################################################################################################
#######################################################################################################
#######################################################################################################


# Exercise 3 : 강남역에 오는 사람들은 어디에서 왔을까?

### step 1 : 2호선 승하차 데이터 중 강남역에서 하차한 데이터만 추출하기
df_line2 = df[(df['승차_호선'] == '2호선') & (df['하차_호선'] == '2호선')]
od_pairs_line2 = df_line2[['승차_역', '하차_역', '총_승객수']].reset_index(drop = True)
od_pairs_line2_toGangnam = od_pairs_line2[od_pairs_line2['하차_역'] == '강남'].reset_index(drop = True)


### step 2 : PolyLine을 이용해서 지도에 선 그리기

map = folium.Map(location = center, zoom_start = 12)

dest_coord = station_coord_dict['강남']
for i in range(len(od_pairs_line2_toGangnam)):
    org_station = od_pairs_line2_toGangnam['승차_역'][i]
    org_coord = station_coord_dict[org_station]
    pax = od_pairs_line2_toGangnam['총_승객수'][i]
    
    arrow_color = 'red' if pax > 1000 else 'blue'
    arrow = folium.PolyLine([org_coord, dest_coord],
                    color = arrow_color,
                    weight = pax / 1000, 
                    arrow_head = 10)
    
    map.add_child(arrow)
    
    folium.CircleMarker(org_coord,
                        radius = 5,
                        color = 'green',
                        fill = True,
                        popup = org_station).add_to(map)
    
    
    
folium.CircleMarker(dest_coord,
                    radius = 5,
                    color = 'purple',
                    fill = True,
                    popup = '강남').add_to(map)

map.save('./to_Gangnam.html')



#######################################################################################################
#######################################################################################################
#######################################################################################################


# Exercise 4 : top10 정류장끼리는 누가 더 많이 왔다갔다?

### step 1 : top10 정류장에 대한 od matrix (or pair) 만들기


#-- ver 1 : Easy but messy
top10_stations = top10['station']
od_pairs_top10 = []
for i in range(len(top10_stations)):
    for j in range(len(top10_stations)):
        
        org_station = top10_stations[i]
        dest_station = top10_stations[j]
        pax = df[(df['승차_역'] == org_station) & (df['하차_역'] == dest_station)]['총_승객수'].sum()
        
        od_pairs_top10.append([org_station, dest_station, pax])

od_pairs_top10 = pd.DataFrame(od_pairs_top10, columns = ['org_station', 'dest_station', 'pax'])


#-- ver 2 : Simple
top10_stations = top10['station']
od_pair_top10 = df[
    df['승차_역'].isin(top10_stations) &
    df['하차_역'].isin(top10_stations)
    ].reset_index(drop = True)

#-- 이용 호선이 다른 경우에도 하나의 값으로 묶어주기
od_pair_top10_combined = od_pair_top10.groupby(['승차_역', '하차_역'])['총_승객수'].sum().reset_index()

### step 2 : PolyLine을 이용해서 지도에 선 그리기
map = folium.Map(location = center, zoom_start = 12)
for i in range(len(od_pairs_top10)):
    org_station = od_pair_top10_combined['승차_역'][i]
    dest_station = od_pair_top10_combined['하차_역'][i]
    pax = od_pair_top10_combined['총_승객수'][i]
    
    org_coord = station_coord_dict[org_station]
    dest_coord = station_coord_dict[dest_station]
    
    arrow_color = 'red' if pax > 2000 else 'blue'
    arrow = folium.PolyLine([org_coord, dest_coord], 
                            color = arrow_color,
                            weight = pax / 1000,
                            arrow_head = 10)
    
    map.add_child(arrow)
    
    folium.CircleMarker(org_coord,
                        radius = 5,
                        color = 'green',
                        popup = org_station,
                        fill = True).add_to(map)

map.save('./demand_top10.html')




#######################################################################################################
#######################################################################################################
#######################################################################################################


# Exercise 5 : 주성분분석을 이용해서 top10 지하철역사간 이동의 주요 패턴 파악하기

### step 1 : OD pair 를 OD matrix 로 바꿔주기
od_matrix_top10 = od_pair_top10_combined.pivot(index = '승차_역', columns = '하차_역', values = '총_승객수')


### step 2 : OD matrix를 SVD로 분해하기
#- step 2-1. OD matrix를 data frame -> 값으로 분해
od_matrix_top10_values = od_matrix_top10.values.astype(float)   # 정수형 -> 실수형

#- step 2-2. rank가 1인 SVD로 분해
from scipy.sparse.linalg import svds

U, sigma, Vt = svds(od_matrix_top10_values, k = 1)

#- step 2-3. sigma를 대각 행렬로 변환
sigma_diag = np.diag(sigma)


### step 3 : 분해된 행렬 복구 (rank 3인 od matrix 만들기)
recon_od_matrix_top10 = np.dot(np.dot(U, sigma_diag), Vt)
recon_od_matrix_top10 = pd.DataFrame(recon_od_matrix_top10, index = od_matrix_top10.index, columns = od_matrix_top10.columns)



### step 4 : 복구된 행렬로 지도에 표출하기
map = folium.Map(location = center, zoom_start = 12)
for i in range(len(recon_od_matrix_top10)):
    for j in range(len(recon_od_matrix_top10)):
        org_station = recon_od_matrix_top10.index[i]
        dest_station = recon_od_matrix_top10.columns[j]
        pax = recon_od_matrix_top10.iloc[i, j]
        
        org_coord = station_coord_dict[org_station]
        dest_coord = station_coord_dict[dest_station]
        
        arrow_color = 'red' if pax > 2000 else 'blue'
        arrow = folium.PolyLine([org_coord, dest_coord], 
                                color = arrow_color,
                                weight = pax / 1000,
                                arrow_head = 10)
        
        map.add_child(arrow)
        
    folium.CircleMarker(org_coord,
                        radius = 5,
                        color = 'green',
                        popup = org_station,
                        fill = True).add_to(map)
    
map.save('./recon_demand_top10_(k=1).html')
