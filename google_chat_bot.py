
from json import dumps

import requests
import asyncio


class GoogleChatBot(object):
    def __init__(self, webhook_url= ''):
        # super(GoogleChatBot, self).__init__(*args)
        self.webhook_url = webhook_url

        self.postToChat_dictKey = 'text'
        self.postToChat_dict = {}
        self.postToChat_dict[self.postToChat_dictKey] = ''

        self.message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    async def post(self,chat_msg_str = ''):

        # await asyncio.sleep(5)

        self.postToChat_dict[self.postToChat_dictKey] = chat_msg_str

        r = requests.post(
            self.webhook_url
            , data = dumps(self.postToChat_dict)
            , headers = self.message_headers
        )

if __name__ == '__main__':
    g = GoogleChatBot('https://chat.googleapis.com/v1/spaces/AAAAnro4QYI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=G1APOmf9POyYF8MqSqZIHVxjk61Mct6Q9FPZUUTMddw%3D')
    asyncio.run( g.post('123456'))