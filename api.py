from googleapiclient.discovery import build
import streamlit as st
# Youtube API settings

API_KEY = st.secrets['ENV']['GOOGLE_API_KEY']
YOUTUBE_API_SERVIVCE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(
    YOUTUBE_API_SERVIVCE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)


def get_video_info(keyword):
  # search settings
  youtube_query = youtube.search().list(
      part='id, snippet',
      q=keyword,
      type='video',
      maxResults=5,
      order='viewCount',
      )
  
  # execute()で検索を実行
  youtube_response = youtube_query.execute()

  # 検索結果を取得し、リターンする
  return youtube_response.get('items',[])