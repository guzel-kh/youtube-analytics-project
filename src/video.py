import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id: str) -> None:
        try:
            self.video_id = video_id
            self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=self.video_id).execute()
            self.title = self.video_response['items'][0]['snippet']['title']
            self.url = 'https://www.youtube.com/watch?v=' + self.video_id
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        except Exception:
            self.video_response = None
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    """Экземпляр инициализируется по 'id видео' и 'id плейлиста'"""
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
