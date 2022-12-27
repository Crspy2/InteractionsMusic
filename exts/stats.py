import interactions
import psutil
import platform

import datetime

from interactions import CommandContext
from interactions.ext.lavalink import VoiceClient

import config


class Stats(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    async def stats(self, ctx: CommandContext):
        """Display the bot's stats"""
        serverCount = len(self.client.guilds)
        try:
            userCount = sum(i.member_count for i in self.client.guilds)
        except:
            userCount = None

        playingServerCount = ctx.client.guilds


        embed = interactions.Embed(title=f"{self.client.me.name}'s stats",
                                   color=config.EMBEDCOLOR)
        embed.set_thumbnail(url=f'{self.client.me.icon_url}')
        embed.add_field(name="Statistics :", value=f"`Servers : {serverCount}\nUsers : {userCount}`", inline=True)
        embed.add_field(name="Using :",
                        value=f"`Python : v{platform.python_version()}\ninteractions.py : v{interactions.__version__}`",
                        inline=True)
        embed.add_field(name="RAM :", value=f"`Used : {psutil.virtual_memory().percent}%`", inline=True)
        embed.add_field(name="Music :", value=f"Playing music on `{playingServerCount}` servers", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.get_avatar_url())
        await ctx.send(embeds=embed)


def setup(client):
    Stats(client)
