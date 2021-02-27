# Hypixel Player Tracker
This simple Python Script, will allow you to get notifications for a player when he connects to the Hypixel Network (Minecraft: Java Edition Server) and do things on it.
## How does it works?
Basically, it just sends requests to [the Hypixel API](http://github.com/HypixelDev/PublicAPI) and detect changes between the responses so it can tell for example that a player joined the server.
Unfortunately, beacause of my lack of skills and also of my laziness, this script is mono-thread and a thread can only listen modifications for one player only.

## Requirements

First of all, you need Python 3.6+ (it could work on lower, but I haven't tested it yet).
Then you need to install 2 dependencies: requests and plyer. Most of Python developers should already have those, but in case you haven't already, install those with pip. Simply use the requirements.txt

```bash
pip install -r requirements.txt
```

(Adapt `pip` if your Python installation is configured differently, like using `pip3` or `python3 -m pip`)

## How to use?

```
Usage: hypixel.py <key> <user>
    <key>: Your Hypixel API Key gathered from mc.hypixel.net (In-Game)
    <user>: The player's name or Mojang UUID. NOTE: It's recommended to use the UUID as the player can 
    change its name in the future or even while the script is running, this could break things.
```
To run this script in background, just use `pythonw`.

```batch
pythonw hypixel.py your-key uuid-or-name
```
You can track multiple player by running multiple instances of the script, but remember that the Hypixel API allows only 120 requests per minutes which is equivalent to 2 requests per second. The more you track players, the more the cooldown value needs to be higher. 
You can change the cooldown by modifying the last line of the script.
A tip that I haven't tested yet, is to create multiple API Key on Hypixel, do it at your own risk.

# ~~*DISCLAIMER*~~
## ~~*This was tested on Windows 10 only and has no guarantee to work on UNIX-like systems (that have desktop environment).*~~
