import os

from interactions.ext.lavalink import VoiceClient


def loadExtensions(client: VoiceClient, directory: str, logger):
    path = os.getcwd()
    exts = [
        module[:-3]
        for module in os.listdir(f"{os.path.dirname(path)}/ProjectLiquid/exts/{directory}")
        if module not in "__init__.py" and module[-3:] == ".py"
    ]

    if exts or exts == []:
        logger.info("Importing %s extensions: %s", len(exts), ", ".join(exts))
    else:
        logger.warning("Could not import any extensions!")

    for ext in exts:
        try:
            client.load(f"exts.{directory}.{ext}")
        except Exception:  # noqa
            logger.error(f"Could not load a {directory} extension: {ext}", exc_info=True)