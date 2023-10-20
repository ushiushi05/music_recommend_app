import numpy as np
import pandas as pd

train = pd.read_csv('data/train.csv')
songs = pd.read_csv('data/songs.csv')
members = pd.read_csv('data/members.csv')
song_ex = pd.read_csv('data/song_extra_info.csv')

merge1 = pd.merge(train, songs, on = 'song_id', how = 'left')
merge2 = pd.merge(merge1, members, on = 'msno', how = 'left')
origin_data = pd.merge(merge2, song_ex, on = 'song_id', how = 'left')

origin_data.isnull().sum()
features = ['name', 'language', 'artist_name', 'composer', 'lyricist']
data = origin_data[features].dropna()
data.info()







