
# KEY variables:
geojson_path= 'C:/Users/Laptop/Documents/Jobb/Geo start-up/Projects/Google_Sheets_API/test/'
csv_path = "C:/Users/Laptop/Documents/Jobb/Geo start-up/Projects/Google_Sheets_API/test/Web_map_points.csv"
service_account_file_path = 'C:/Users/Laptop/Documents/Jobb/Geo start-up/Projects/Google_Sheets_API/test/KEY_sheets_API_test.json'
df_new_path = 'C:/Users/Laptop/Documents/Jobb/Geo start-up/Projects/Google_Sheets_API/test/sheets_to_csv_test.csv'
df_old_path = "C:/Users/Laptop/Documents/Jobb/Geo start-up/Projects/Google_Sheets_API/test/Web_map_points.csv"

SPREADSHEET_ID = '1qvUguizcGvMqC2u9CmO2PJMJ0IvOm91xn1nj3F3eov8'

PATH_OF_GIT_REPO = 'C:/Users/Laptop/Documents/Jobb/Geo start-up/Projects/Google_Sheets_API/test/.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'comment from python script'


# Tuturial followed https://www.youtube.com/watch?v=4ssigWmExak

import pandas as pd

from googleapiclient.discovery import build
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

creds = service_account.Credentials.from_service_account_file(service_account_file_path, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range="Vaccinations!A1:G500").execute()
values = result.get('values', [])

# make dataframe from sheets values
df = pd.DataFrame(values[1:], columns = values[0])

df.to_csv(df_new_path, index=False)


from geojson import Feature, FeatureCollection, Point
import json
import numpy as np

# CSV to Geojson function

from git import Repo


def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        print('1', repo)
        repo.git.add(update=True)
        print('2')
        repo.index.commit(COMMIT_MESSAGE)
        print('3')
        origin = repo.remote(name='origin')
        print('4')
        origin.push().raise_if_error()
    except:
        print('Some error occured while pushing the code')    



def CSV_to_Geojson():

    df_from_csv = pd.read_csv(csv_path)

    def lat_func(row):  
            try: 
                lat = row['coordinates'].split(',')[1]
                return lat
            except:
                print('WARNING: row missing coordinates')
                lat = np.nan
                return lat
        
    def lng_func(row):
            try: 
                lng = row['coordinates'].split(',')[0]
                return lng
            except:
                lng = np.nan
                print('WARNING: row missing coordinates')
                return lng
            
    df_from_csv['lat'] = df_from_csv.apply(lambda row: lng_func(row), axis=1)
    df_from_csv['lng'] = df_from_csv.apply(lambda row: lat_func(row), axis=1)

    df_from_csv['lat'] = df_from_csv['lat'].astype(float)
    df_from_csv['lng'] = df_from_csv['lng'].astype(float)


    # geometry filtering
    geometry = df_from_csv.apply(
        lambda row: Feature(geometry=Point((float(row['lng']), float(row['lat'])))),
        axis=1).tolist()

    # all the other columns used as properties
    properties = df_from_csv.drop(['lat', 'lng'], axis=1).to_dict('records')

    # make feature list
    features_list = []
        
    for i, x in zip(geometry, properties):
        i2 = i  
        i2['properties'] = x
        features_list.append(i)

    #print('features_list first item:', features_list[0])

    # Export geojson as feature collection
    feature_collection = FeatureCollection(features_list)

    with open(f'{geojson_path}geojson_test.geojson', 'w', encoding='utf-8') as f:
        json.dump(feature_collection, f, ensure_ascii=False)
    


df_new = pd.read_csv(df_new_path, index_col='ID')
print(df_new)

df_old = pd.read_csv(df_old_path, index_col='ID')
print(df_old)

if df_old.equals(df_new):
    print('The same')
    
else:
    df_new.to_csv(df_old_path) # overwrite old csv with new
    CSV_to_Geojson() # overwrite old geojson with new
    print('NOT the same')


df_new2 = pd.read_csv(df_new_path, index_col='ID')

df_old2 = pd.read_csv(df_old_path, index_col='ID')


if df_old2.equals(df_new2):
    print('The same')
    

else:
    print('NOT the same')


try:
    print('git_push')
    git_push()
except:
    print('NO_git_push')