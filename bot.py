#! /usr/bin/env python
import configparser
import datetime
import logging
import sys
import time

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

        self.check_interval = int(config['Bot']['CheckInterval'])

        self._last_message_sent_date = None

    def is_new_day(self) -> bool:
        """Return True when it's a new day since the last time a message was sent"""
        today = datetime.date.today()
        if self._last_message_sent_date:
            if self._last_message_sent_date < today:
                logging.info("It's a new day! The sun could be shining")
                return True
            else:
                return False
        else:
            return True

    def loop(self):
        while True:
            try:
                self.check_electricity_live()
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                break


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
            if self.is_new_day():
                self.send_message(f'Now generating {returned}W but only using {delivered}W, so you have {surplus}W extra')
                self._last_message_sent_date = datetime.date.today()
            else:
                logging.info("Generating surplus over threshold but already sent a message")
        else:
            logging.info(f'Now generating {returned}W but using {delivered}W, so you have {surplus}W short')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s]: %(message)s')

    bot = SurplusBot(config)

    bot.loop()