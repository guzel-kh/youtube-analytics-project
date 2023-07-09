import os

from datetime import timedelta

import isodate

from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')

    youtube = build('youtube', 'v3', developerKey=api_key)

    channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.youtube.playlists().list(id=self.playlist_id,
                                                   part='snippet,contentDetails',
                                                   maxResults=50
                                                   ).execute().get('items')[0].get('snippet').get('title')
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

        # self.playlists = self.youtube.playlists().list(channelId=PlayList.channel_id,
        #                                           part='contentDetails,snippet',
        #                                           maxResults=50,
        #                                           ).execute()
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
        total_duration = timedelta()

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        for video_id in self.video_ids:
            best = 0
            video_response = self.youtube.videos().list(part='statistics',
                                                        id=video_id).execute()
            like_count = video_response['items'][0]['statistics']['likeCount']
            if int(like_count) > best:
                best = "https://youtu.be/" + video_id
        return best
