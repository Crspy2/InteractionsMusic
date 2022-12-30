import logging
import os

import interactions
import tekore
from interactions import Intents
from interactions.ext.lavalink import VoiceClient

import config
from utils import logutil
from utils.loadExtensions import loadExtensions


logger = logutil.init_logger("main.py")
logger.debug(
    "Debug mode is %s; This is not a warning, just an indicator. You may safely ignore",
    config.DEBUG,
)

client = VoiceClient(
    token=os.environ.get("TOKEN"),
    intents=Intents.GUILD_VOICE_STATES,
    default_scope=1033179010487812127,
    logging=logging.DEBUG,
)


@client.event
async def on_ready():
    logger.info("Logged in")

if config.spotifyClientID != "":
    spotifyAppToken = tekore.request_client_token(config.spotifyClientID, config.spotifyClientSecret)
    client.spotify = tekore.Spotify(spotifyAppToken, asynchronous=True)
    client.playlistLimit = 20

# Import Extentions
loadExtensions(client, "music", logger)

client.load("interactions.ext.enhanced")

client.start()
