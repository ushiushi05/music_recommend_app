import streamlit as st
import pandas as pd
import numpy as np
import collections

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