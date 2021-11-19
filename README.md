# energy-surplus-telegram-bot
Get sent a notification when your solar panel are generating more than you use

<img src="https://user-images.githubusercontent.com/709259/142645240-04a0295d-623c-4c30-b93c-de13b90779d8.jpeg" width="300" alt="screenshot"/>

## Usage:

0. Clone the repository
1. Set up DSMR Reader per the link in the repository description. You'll need a Dutch Smart Meter compatible energy meter and a proper cable to connect to the meter's P1 port.
2. Get the API key for DSMR Reader via eg. http://raspberrypi.local/admin/dsmr_api/apisettings/1/change/ (if raspberrypi.local is where the DSMR Reader is running)
3. Get a Telegram bot API key via Telegram's BotFather https://t.me/botfather
4. Copy example.ini to eg. `home.ini` and edit the values in `home.ini` to your needs. You put the Telegram API key in there as well.
5. Run `./bot.py home.ini --log=INFO`
