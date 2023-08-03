import datetime
from datetime import datetime, timedelta
import os
import isodate
from googleapiclient.discovery import build


api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id

        playlists = youtube.playlists().list(id=playlist_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()

        self.title = playlists["items"][0]["snippet"]["title"]
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @property
    def total_duration(self):
        playlist_id = self.playlist_id
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        now = datetime.now()
        total_duration = datetime.now()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        total_duration -= now
        s = timedelta.total_seconds(total_duration)
        total_duration = timedelta(seconds=int(s))

        return total_duration

    def show_best_video(self):
        playlist_id = self.playlist_id
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        max_like_count = 0
        video_id = ""

        for video in video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like_count:
                max_like_count = int(video['statistics']['likeCount'])
                video_id = video['id']

        video_url = 'https://youtu.be/' + video_id

        return video_url

