import pandas as pd
import folium
import json
import re

file = pd.read_csv("atms_with_counties.csv")
print(file)

diacritics = {'ş': 'ș', 'ţ':'ț'}

filter_dict = {
    "banca transilvania" : "BT",
    "cec bank" : "CEC",
    "bcr" : "BCR",
    "brd groupe societe generale" : "BRD",
    "brd" : "BRD",
    "raiffeisen bank" : "Raiffeisen",
    "raiffeisen" : "Raiffeisen",
    "unicredit bank" : "UniCredit",
    "unicredit" : "UniCredit",
    "garanti" : "Garanti",
    "otp" : "OTP",
    "ing" : "ING",
    "euronet" : "Euronet",
    "patria" : "Patria",
    "intesa" : "Intesa Sanpaolo",
    "bitcoin" : "Bitcoin",
    "banca românească" : "EXIM",
    "romaneasca": "EXIM",
    "exim": "EXIM",
    "raiff" : "Raiffeisen",
    "alpha bank" : "Alpha",
    "c.e.c. bank" : "CEC",
    "bt" : "BT",
    "otpbank" : "OTP",
    "libra" : "Libra Internet",
    "first": "First",
    "transilania" : "BT",
    "cek": "CEC",
    "crypto" : "Bitcoin",
    "tech": "Techventures",
    "ventures": "Techventures"
}

Colors = {'BT': 'black',
          'CEC': 'ForestGreen',
          'BCR': 'DodgerBlue',
          'BRD': 'Crimson',
          'Raiffeisen': 'Gold',
          'UniCredit': 'Red',
          'Altele': 'Fuchsia',
          'Alpha': 'CornflowerBlue',
          'OTP': 'OliveDrab',
          'Garanti': 'SpringGreen',
          'Bitcoin': 'Khaki',
          'ING': 'Orange',
          'Patria': 'Navy',
          'Euronet': 'RoyalBlue',
          'Intesa Sanpaolo': 'DarkGreen',
          'Techventures': 'LightSlateGray',
          'Libra Internet': 'Salmon',
          'EXIM': 'SkyBlue',
          'First': 'Blue'
          }

file.drop_duplicates(subset=["name_left", "latitude", "longitude"], inplace=True)

for index, row in file.iterrows():
    found = False
    for key, value in filter_dict.items():
        if key in row["name_left"].lower():
            file.loc[index, "name_left"] = value
            found = True
    if not found:
        file.loc[index, "name_left"] = "Altele"
        
pd.set_option("display.max_rows", None)
print(file["name_left"].value_counts())

file.to_csv('atms_with_counties_cleaned.csv', index=False)

nuts_file = open('NUTS_2.geojson', encoding="utf-8")
nuts = json.load(nuts_file)

m = folium.Map(location=(45.9432, 24.9668), zoom_start=7)

new_features = {'type': 'FeatureCollection', 'features': [], 'crs': nuts['crs']}

atm_count = file['county'].value_counts()

population_data = pd.read_excel("eurostat_demographics.xlsx", 2)

income_data = pd.read_excel("eurostat_demographics.xlsx", 3)

employment_data = pd.read_excel("eurostat_demographics.xlsx", 4)

productivity_data = pd.read_excel("eurostat_demographics.xlsx", 5)

age_data = pd.read_excel("eurostat_demographics.xlsx", 6)

for nuts_features in nuts['features']:
    if 'RO' in nuts_features['id'] and nuts_features['id'] != 'RO' and int(re.findall('\d+|\D+', nuts_features['id'])[-1]) > 100:
        nuts_features['properties']['atm'] = int(atm_count.loc["".join([diacritics[char] if char in diacritics else char for char in nuts_features['properties']['NUTS_NAME']])])
        nuts_features['properties']['population'] = population_data[population_data['County'] == nuts_features['properties']['NUTS_NAME']].values[0][1]
        nuts_features['properties']['income'] = income_data[income_data['County'] == nuts_features['properties']['NUTS_NAME']].values[0][1]
        nuts_features['properties']['employment'] = employment_data[employment_data['County'] == nuts_features['properties']['NUTS_NAME']].values[0][1]
        nuts_features['properties']['age'] = age_data[age_data['County'] == nuts_features['properties']['NUTS_NAME']].values[0][1]
        nuts_features['properties']['productivity'] = productivity_data[productivity_data['County'] == nuts_features['properties']['NUTS_NAME']].values[0][1]

        new_features['features'].append(nuts_features)

tooltip=folium.GeoJsonTooltip(
    fields=["NAME_LATN", 'atm', 'population', 'income', 'employment', 'age', 'productivity'], 
    aliases=["County: ", "Number of ATMs: ", "Avg annual population: ", "GDP per inhabitant, in euro: ", 'Employment: ', 'Population 65+ to population 20-64: ', 'Nominal labour productivity: '],     
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 1px solid black;
        border-radius: 2px;
        box-shadow: 3px;
    """,
)

folium.GeoJson(data=new_features,  
               highlight_function= lambda feat: {'fillColor': 'PaleGoldenrod', 'fillOpacity': 0.6, 'stroke': False}, 
               style_function=lambda feature: 
               {
                "fillColor": None,
                "fillOpacity": 0.1,
                "weight": 1,
                "opacity": 0.6,
                "color": "gray"
            },
                tooltip=tooltip,
                stroke=False
                ).add_to(m)

# for nuts_features in nuts['features']:
#     if 'RO' in nuts_features['id'] and nuts_features['id'] != 'RO' and int(re.findall('\d+|\D+', nuts_features['id'])[-1]) > 100:
#         if len(nuts_features['geometry']['coordinates']) == 1:
#             coord_set = nuts_features['geometry']['coordinates'][0]
#             coord_set = [[coord[1], coord[0]] for coord in coord_set]
#             folium.Polygon(
#                 locations=coord_set,
#                 color="#FF0000",
#                 weight=5,
#                 fill_color="black",
#                 fill_opacity=0.1,
#                 tooltip=nuts_features['properties']['NAME_LATN']
#             ).add_to(m)
#         else:
#             for large_coord_set in nuts_features['geometry']['coordinates']:
#                 if len(large_coord_set[0]) == 2:
#                     large_coord_set = [[coord[1], coord[0]] for coord in large_coord_set]
#                     folium.Polygon(
#                         locations=large_coord_set,
#                         color="#FF0000",
#                         weight=5,
#                         fill_color="black",
#                         fill_opacity=0.1,
#                         tooltip=nuts_features['properties']['NAME_LATN']
#                     ).add_to(m)
#                 else:
#                     for small_coord_set in large_coord_set:
#                         small_coord_set = [[coord[1], coord[0]] for coord in small_coord_set]
#                         folium.Polygon(
#                             locations=small_coord_set,
#                             color="#FF0000",
#                             weight=5,
#                             fill_color="black",
#                             fill_opacity=0.1,
#                             tooltip=nuts_features['properties']['NAME_LATN']
#                         ).add_to(m)

for index, row in file.iterrows():
    folium.CircleMarker(
    location=[row['latitude'], row['longitude']],
    tooltip=row["name_left"],
    color=Colors[row["name_left"]],
    radius=4,
    fill=True
    ).add_to(m)
    


m.save('romania.html')