import time # For requests cooldown. Remember, you can only do 120 requests per minute with Hypixel API.
import requests as query # HTTP Requests
from plyer import notification # To display notifications, works on Windows, not tested on UNIX-like systems.

import sys
import traceback


# Those variables will manage how notifications
# are sent depending on if they're connected, 
# if they are playing a game etc.
global previouslyConnected
global playerSession
previouslyConnected=False 
playerSession={}

global api_key
global playerName

playerName = ""

api_key = ""

# This HTTP Header is required by Hypixel API, as they want to do some statistics and prevent API Abuse.
global headers
headers={"user-agent": "python/{}".format(".".join([str(sys.version_info[0]), str(sys.version_info[1]), str(sys.version_info[2])]))}

# This will prevent providing too much or too less arguments.
if len(sys.argv) <= 1 or sys.argv == None or len(sys.argv)>=4:
    print(sys.argv)
    print("""Usage: py | python | python3 {} <key> <user>
    <key>: Your Hypixel API Key gathered from mc.hypixel.net (In-Game)
    <user>: The player's name or Mojang UUID. NOTE: It's recommended to use the UUID as the player can 
    change its name in the future or even while the script is running, this could break things.
    """.format(__file__))

    sys.exit()

# Checking the API Key
# The body should look like this:
# {
#     "sucess": boolean,
#     "record": {
#         "key": string,
#         "owner": string (uuid),
#         "limit": integer,             // Limtit of requests per minute
#         "queriesInPastMin": integer,  // Does not include this query
#         "totalQueries": integer
#     }
# }
try:
    
    keyQuery=query.get(f"https://api.hypixel.net/key", params={"key": sys.argv[1]}, headers=headers)
    
    if keyQuery.json()["success"]:
        print(f"""Your key is valid.
        You have {keyQuery.json()["record"]["limit"]-keyQuery.json()["record"]["queriesInPastMin"]} queries left for this minute.""")
        api_key = sys.argv[1]
    
    else:
        print("Your API Key is invalid.")
        print(f"""
        ========== TRACEBACK ==========
        Error source: HTTP
        Request URL: {keyQuery.url}
        Request status: {keyQuery.status_code}
        Request response body:
        {keyQuery.json()} 
        """)
        sys.exit()

except Exception as e:
    
    traceb="\n".join(traceback.extract_tb(e.__traceback__).format())

    print(f"""There was an error while trying to reach Hypixel API. Is your connection ok?

    ========== TRACEBACK ==========
    Error source: Python
    Traceback:
    {traceb}""")

global uuid
uuid = ""


# From the arguments, it will try to get the UUID in any ways. If the UUID
# is provided, it will use it directly, if not, it will search for the
# right player and gather the UUID from Hypixel's (Mojang) database.
try:
    
    nameQuery=query.get(f"https://api.hypixel.net/player", params={"key": api_key, "name": sys.argv[2]}, headers=headers)
    
    if nameQuery.json()["success"] and nameQuery.json()["player"]!=None:
        
        uuid = nameQuery.json()["player"]["uuid"]
        ## print(uuid)
        playerName = nameQuery.json()["player"]["displayname"]
        raise DeprecationWarning("It is not recommended to use Usernames as it could change while the process is running.") # This raise is intended to break the try block.
                                                                                                                            # I know it's cheesy but it's the only way I
                                                                                                                            # found make this work.

    uuidQuery=query.get(f"https://api.hypixel.net/player", params={"key": api_key, "uuid": sys.argv[2]}, headers=headers)
    
    if uuidQuery.json()["success"]:
        
        uuid = sys.argv[2]
        ## print(uuid)
        ## print(uuidQuery.url)
        playerName = uuidQuery.json()["player"]["displayname"]
    
    else:
        
        print(f"""The UUID is malformed or the player does not exists.

========== TRACEBACK ==========
Error source: HTTP
Requests URLs: {nameQuery.url}, {uuidQuery.url}
Requests Statuses: {nameQuery.status_code}, {uuidQuery.status_code}

Userame Method Request Response:
{nameQuery.json()}

UUID Method Request Response:
{uuidQuery.json()}""")
        
        sys.exit()

except DeprecationWarning as e:
    
    print(e)
    
    ask=input("Would you like to run this method (at your own risk) anyways? [y/N]: ")
    
    if ask.upper() not in ["Y", "YES", "YE", "YEAH"]: # Don't question this please.
        sys.exit()

except Exception as e:
    traceb="\n".join(traceback.extract_tb(e.__traceback__).format())

    print(f"""There was an error while trying to reach Hypixel API. Is your connection ok?

    ========== TRACEBACK ==========
    Error source: Python
    Traceback:
    {traceb}""")
    
## print(uuid)

if __name__!="__main__":
    raise ImportError("This file is not meant to be used as a module.")


# while True? Nah, that's for poor people, we are
# aristocrats here.
while __name__=="__main__":
    
    try:
        
        mainQuery=query.get(f"https://api.hypixel.net/status", params={"key": api_key, "uuid": uuid}, headers=headers)
        ## print(mainQuery.url)
        requestSession=mainQuery.json()["session"]
        
        if mainQuery.json()["session"]["online"]: # This is value is a boolean so it's ok for Python to do this.
            
            # IF the player wasn't connected before the request, it will send a notification.
            if not previouslyConnected:
                notification.notify(
                    title = "Hypixel Player Tracker",
                    message = f"{playerName} is now online on the network!",
                    app_icon = "hypixel.ico", # Fun fact: I just took the Base64 image from Minecraft NBT data, converted it into JPG, then into ICO
                    timeout = 3

                )
                previouslyConnected=True # And we make sure to change it to prevent spam.

            # This will send a notification everytime a player is joining a BungeeCord server (games, lobby etc.).
            # If you find this too "spammy", feel free to make a pull request and improve the code. I'm too lazy
            # to do that ngl.
            elif playerSession != mainQuery.json()["session"]:
                playerSession = mainQuery.json()["session"]
                gameType = playerSession["gameType"]
                mode = playerSession["mode"]
                notification.notify(
                    title = "Hypixel Player Tracker",
                    message = f"{playerName} is now playing {gameType} ({mode})",
                    app_icon = "hypixel.ico",
                    timeout = 3
                )
        else:
            if previouslyConnected:
                notification.notify(
                    title = "Hypixel Player Tracker",
                    message = f"{playerName} disconnected from the Network.",
                    app_icon = "hypixel.ico",
                    timeout = 3
                )
            previouslyConnected=False # When the player disconnects we make sure this changes so that the notification will trigger again.
    
    except Exception as e:
        traceb="\n".join(traceback.extract_tb(e.__traceback__).format())

        print(f"""There was an error while trying to reach Hypixel API. Is your connection ok?

        ========== TRACEBACK ==========
        Request url: {mainQuery.url}
        Error source: Python
        Traceback:
        {traceb}""")
    time.sleep(2.5) # This value will prevent from doing too many requests. But surprisingly, it's super responsive!
                    # You can change this value if you want to prevent rate limit.

## EOF