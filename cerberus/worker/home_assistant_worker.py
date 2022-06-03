from requests import get, post, Response
from urllib.parse import urljoin
from time import sleep
import threading
from cerberus.command_event import CommandEvent
from cerberus.worker import TCSCommunicator
from cerberus.const import *

class HomeAssistantWorker:
    _tcs_communicator: TCSCommunicator
    _url: str
    _google_home_entity_id: str
    _doorbell_media: dict
    _headers: dict

    _requests: dict = {}

    def __init__(self, tcs_communicator: TCSCommunicator, url: str, api_token: str, google_home_entity_id: str, doorbell_media: dict = {'downstairs': '/media/media/doorbell.mp3', 'upstairs': '/media/media/doorbell.mp3'}):
        threading.Thread.__init__(self)

        self._tcs_communicator = tcs_communicator
        self._url = url
        if not self._url.endswith('/'):
            raise Exception('URL must end in \'/\'')
        self._google_home_entity_id = google_home_entity_id
        self._doorbell_media = doorbell_media
        self._headers = {
            "Authorization": "Bearer %s" % (api_token),
            "Content-Type": "application/json",
        }

        self._subscription = self._tcs_communicator.command_read.subscribe(
            on_next = self.command_read
        )

    def prepare_commands(self) -> None:
        self._requests[COMMANDS[RING_UPSTAIRS]]['fn'] = self.send_ring_upstairs
        self._requests[COMMANDS[RING_DOWNSTAIRS]]['fn'] = self.send_ring_downstairs

    def command_read(self, command_event: CommandEvent) -> None:
        command_value = command_event.cmd
        if not command_value in self._requests:
            return

        print('Home Assistant Worker Recieved: ' + command_value)
        command = self._requests[command_value]
        command['fn']()

    def send_ring_upstairs(self) -> None:
        self.__ring(self._doorbell_media['downstairs'])
        sleep(3)
        self.__announce('Someone\'s at the door downstairs.')

    def send_ring_downstairs(self) -> None:
        self.__ring(self._doorbell_media['upstairs'])
        sleep(3)
        self.__announce('Someone\'s at the front door.')

    def __ring(self, media: str) -> Response:
        return post(urljoin(self._url, 'services/media_player/play_media'), headers=self._headers, json={
            'entity_id': self._google_home_entity_id,
            'media_content_id': media,
            'media_content_type': 'audio/mp3'
        })

    def __announce(self, text: str) -> Response:
        return post(urljoin(self._url, 'services/tts/google_translate_say'), headers=self._headers, json={
            'entity_id': self._google_home_entity_id,
            'message': text
        })