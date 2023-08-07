from googleapiclient.discovery import build

import os

api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для видео"""

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        try:
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()

            self.title: str = video_response['items'][0]['snippet']['title']
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
            self.video_url = 'https://youtu.be/' + self.video_id
        except IndexError:
            self.title = None
            self.view_count = None
            self.like_count = None
            self.video_url = None

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
