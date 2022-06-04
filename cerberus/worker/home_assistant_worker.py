from requests import get, post, Response
from urllib.parse import urljoin
from time import sleep
import threading
from cerberus.command_event import CommandEvent
from cerberus.worker import TCSCommunicator
from cerberus.const import *
from reactivex import operators as op

class HomeAssistantWorker:
    _tcs_communicator: TCSCommunicator
    _url: str
    _google_home_entity_id: str
    _doorbell_media: dict
    _headers: dict

    _requests: dict = HOME_ASSISTANT_COMMANDS

    def __init__(self, tcs_communicator: TCSCommunicator, url: str, api_token: str, google_home_entity_id: str, doorbell_media: dict):
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

        self.prepare_commands()
        
        print('Starting Home Assistant')
        self._subscription = self._tcs_communicator.command_read.pipe(
            op.debounce(0.2)
        ).subscribe(
            on_next = self.command_read
        )

    def prepare_commands(self) -> None:
        self._requests[RING_UPSTAIRS]['fn'] = self.send_ring_upstairs
        self._requests[RING_DOWNSTAIRS]['fn'] = self.send_ring_downstairs

    def command_read(self, command_event: CommandEvent) -> None:
        command_value = command_event.cmd
        if not command_value in self._requests:
            return

        print('Home Assistant Worker Recieved: %s' % (hex(command_value)))
        command = self._requests[command_value]
        command['fn']()

    def send_ring_upstairs(self) -> None:
        self.__ring(self._doorbell_media['downstairs'])
        sleep(3)
        self.__announce('Someone\'s at the front door.')

    def send_ring_downstairs(self) -> None:
        self.__ring(self._doorbell_media['upstairs'])
        sleep(3)
        self.__announce('Someone\'s at the door downstairs.')

    def __ring(self, media_dict: dict) -> Response:
        return post(urljoin(self._url, 'services/media_player/play_media'), headers=self._headers, json={
            'entity_id': self._google_home_entity_id,
            'media_content_id': media_dict['media'],
            'media_content_type': media_dict['type']
        })

    def __announce(self, text: str) -> Response:
        return post(urljoin(self._url, 'services/tts/google_cloud_say'), headers=self._headers, json={
            'entity_id': self._google_home_entity_id,
            'message': text
        })