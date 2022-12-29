import logging
import os
import sys

import interactions
import tekore
from interactions import Intents
from interactions.ext.lavalink import VoiceClient

import config
from utils import logutil

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
exts = [
        module[:-3]
        for module in os.listdir(f"{os.path.dirname(__file__)}/exts")
        if module not in ("__init__.py", "template.py") and module[-3:] == ".py"
    ]

if exts or exts == []:
    logger.info("Importing %s cogs: %s", len(exts), ", ".join(exts))
else:
    logger.warning("Could not import any cogs!")

for ext in exts:
    try:
        client.load(f"exts.{ext}")
    except Exception:  # noqa
        logger.error(f"Could not load a cog: {ext}", exc_info=True)

client.load("interactions.ext.enhanced")

client.start()
