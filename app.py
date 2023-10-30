import streamlit as st
import pandas as pd
import numpy as np
import collections
from api import get_video_info
st.set_page_config(
  page_title='レコミュー',
  page_icon='🎧'
)
st.title('音楽レコメンド')

# 楽曲情報の読み込み
music = pd.read_csv("data/data.csv")

# 楽曲情報データ
music_data = music.drop('user_id', axis=1)
music_data = music_data.drop_duplicates().sort_values('song_name').reset_index(drop=True)

# アプリで4種類から選択できるようにする
song_name = sorted(list(set(music['song_name'].tolist())))
artist = sorted(list(set(music['artist_name'].tolist())))
composer = sorted(list(set(music['composer'].tolist())))
lyricist = sorted(list(set(music['lyricist'].tolist())))

# userが聞いた曲のdf
unique = music.groupby('user_id').agg({'song_name': list})
listened_list = unique['song_name'].tolist()


st.markdown("### 1つの楽曲に対して他のユーザーが聞いた楽曲を表示します")
selected_music = st.selectbox("楽曲を選んでください", song_name)

howmany_length = st.slider("どのくらいの曲数を表示しますか", 1, 10)
st.divider()
music_info = music_data[music_data["song_name"].isin([selected_music])]

st.write(f"#### あなたが選択した楽曲は【{selected_music}】です。楽曲の情報は下記のようになります")
st.table(music_info)

# 趣味が似ているユーザーの聞いた楽曲を表示
threshold = 2
st.markdown(f"#### 【{selected_music}】を聞いた人はこの楽曲も聴いています")
results = []
for i in range(len(listened_list)):
  if selected_music in listened_list[i]:
    if len(listened_list[i]) > threshold:
      results += listened_list[i]
c = collections.Counter(results)
values, counts = zip(*c.most_common(howmany_length))

recommend_df = pd.DataFrame()
for j in range(len(values)):
  recommend_info = music_data[music_data['song_name'].isin([values[j]])]
  df_new = pd.DataFrame(recommend_info)
  recommend_df = pd.concat([recommend_df, df_new])

st.table(recommend_df)

# 選んだ楽曲をyoutubeで検索する
to_youtube = st.selectbox("YouTubeで検索する楽曲を選んでください", recommend_df['song_name'])
youtubes = get_video_info(to_youtube)

title_url_df = pd.DataFrame()
for l in range(len(youtubes)):
  video_title = youtubes[l]['snippet']['title']
  videoId = youtubes[l]['id']['videoId']
  videoDf = pd.DataFrame({'title': video_title, 
                          'id':videoId},
                          index=['#'])
  title_url_df = pd.concat([title_url_df, videoDf])

# タイトルとIDを表示して、IDを選択する
st.table(title_url_df)

url = 'https://www.youtube.com/watch?v='
selected_id = st.selectbox("idを選んでください", title_url_df['id'])
url += selected_id
st.link_button("YouTubeへ移動します！", url)

