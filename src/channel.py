import json
import os

from googleapiclient.discovery import build


api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.subscriberCount = channel["items"][0]["statistics"]["subscriberCount"]
        self.url = "https://www.youtube.com/channel/"+self.__channel_id
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.viewCount = channel["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def channel_id(self, channel_id):
        self.__channel_id = channel_id

    def to_json(self, file_json):
        with open(file_json, 'wt') as file:
            channel = {'channel_id': self.__channel_id, 'title': self.title, 'description': self.description,
                       'subscriberCount': self.subscriberCount, 'url': self.url, 'video_count': self.video_count,
                       'viewCount': self.viewCount}
            file.write(json.dumps(channel, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))