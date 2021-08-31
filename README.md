# saegl-bot-2021

This project is a collection of plugin modules for the maubot
(https://github.com/maubot/maubot). Matrix chat bot framework.
These modules are/were intendded for use by the Seattle GNU/Linux
conference (SeaGL) conference.


# Setup Maubot:
0. Consider the production instructions at: https://docs.mau.fi/maubot/usage/setup/index.html
   These instructions are not perfect. :( But steps 1,2,3,7,6 are key.

1. As instructed in step 0, Start the bot by running: 
	`source ./bin/activate`
	`python3 -m maubot`

2. Run the following commands to login the bot, and get a device token.
   Save the token, as you will need it for setting up your instance.
	Run: `mbc login`
	Run: `mbc auth`

3. Connect to: http://192.168.1.111:29316/_matrix/maubot/#/
   and login

4. Install your plugins

5. Setup your client. Use your device token here.
   NOTE: In order to access your homeserver in the drop-down
         add your homeserver name to your config.yaml
         under 'Shared registration secrets...'.
	* User ID: @seagl-bot:seattlematrix.org
    * Homeserver: seattlematrix.org

6. Setup your instance
	* ID: seagl-bot
	* Primary User: __
	* Type: __


