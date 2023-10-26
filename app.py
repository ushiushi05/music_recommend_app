import streamlit as st
import pandas as pd
import numpy as np
import gensim
import collections

st.set_page_config(
  page_title='レコミュー',
  page_icon='🎧'
)
st.title('音楽レコメンド')

# 楽曲情報の読み込み
music = pd.read_csv("data/data.csv")

music_data = music.drop('user_id', axis=1)
music_data = music_data.drop_duplicates().sort_values('song_name')
# アプリで4種類から選択できるようにする
song_name = sorted(list(set(music['song_name'].tolist())))
artist = sorted(list(set(music['artist_name'].tolist())))
composer = sorted(list(set(music['composer'].tolist())))
lyricist = sorted(list(set(music['lyricist'].tolist())))
length = range(1, 11)
# userが聞いた曲のdf
unique = music.groupby('user_id').agg({'song_name': list})
listened_list = unique['song_name'].tolist()


st.markdown("## 1つの楽曲に対して他のユーザーが聞いた楽曲を表示します")
selected_music = st.selectbox("楽曲を選んでください", music_data['song_name'])
selected_length = 3
howmany_length = st.selectbox("どのくらいの曲数を表示しますか", length)
st.write(f"あなたが選択した楽曲は{selected_music}です")
# st.write(f'あなたが選んだ楽曲の情報は{music_data[selected_music]}')
# 趣味が似ているユーザーの聞いた楽曲を表示
st.markdown(f"### {selected_music}を聞いた人はこの楽曲も聴いています")
results = []
for i in range(len(listened_list)):
  if selected_music in listened_list[i]:
    if len(listened_list[i]) > selected_length:
      results += listened_list[i]
c = collections.Counter(results)
values, counts = zip(*c.most_common(howmany_length))

st.write(values)


# st.markdown("## 複数の楽曲を選んでおすすめの楽曲を表示する")

# selected_music = st.multiselect("楽曲を複数選んでください", song_name)
# selected_music_ids = [song_name_to_id[music] for music in selected_music]
# vectors = [model.wv.get_vector(music_id) for music_id in selected_music_ids]
# if len(selected_music) > 0:
#     user_vector = np.mean(vectors, axis=0)
#     st.markdown(f"### おすすめの楽曲")
#     recommend_results = []
#     for music_id, score in model.wv.most_similar(user_vector):
#         title = music_id_to_title[music_id]
#         recommend_results.append({"music_id":music_id, "title": title, "score": score})
#     recommend_results = pd.DataFrame(recommend_results)
#     st.write(recommend_results)
