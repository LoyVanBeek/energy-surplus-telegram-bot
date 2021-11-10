#! /usr/bin/env python
import configparser
import sys

import requests
from telegram.ext import Updater


class SurplusBot:
    def __init__(self, config):
        self.surplus_threshold = int(config['Surplus']['Threshold'])
        self.dsmrreader_api_key = config['DSMRReader']['ApiKey']
        self.telegram_api_key = config['Telegram']['ApiKey']
        self.telegram_chat_id = config['Telegram']['ChatID']
        self.dsmrreader_elec_live_url = config['DSMRReader']['ElecLiveURL']

        self.telegram_updater = Updater(token=self.telegram_api_key,
                                        use_context=True)


    def send_message(self, message: str):
        self.telegram_updater.bot.send_message(text=message, chat_id=self.telegram_chat_id)


    def check_electricity_live(self):
        r = requests.get(self.dsmrreader_elec_live_url, 
                         headers={'X-AUTHKEY': self.dsmrreader_api_key, 
                                  'AUTHORIZATION': 'Token key'})
        data = r.json()

        delivered = data['currently_delivered']  # [Watt]
        returned = data['currently_returned']  # [Watt]
        surplus = returned - delivered

        if surplus >= self.surplus_threshold:
            self.send_message(f'Now generating {returned}W but only using {delivered}W, so you have {surplus}W extra')
        else:
            self.send_message('You are using power but not generating a reasonable surplus')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    bot = SurplusBot(config)

    bot.check_electricity_live()