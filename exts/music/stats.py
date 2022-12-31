import interactions
import psutil
import platform

from interactions import CommandContext
from interactions.ext.lavalink import VoiceClient

import config


class Stats(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    async def stats(self, ctx: CommandContext):
        """Display the bot's stats"""
        embed = interactions.Embed(title=f"{self.client.me.name}'s stats",
                                   color=config.EMBEDCOLOR)
        embed.set_thumbnail(url=f'{self.client.me.icon_url}')
        embed.add_field(name="__**Statistics:**__",
                        value=f"**Servers:** `{len(self.client.guilds)}`", inline=True)
        embed.add_field(name="__**Using**__:",
                        value=f"**Python:** `v{platform.python_version()}`\n**interactions.py**: `v{interactions.__version__}`",
                        inline=True)
        embed.add_field(name="__**RAM**__:",
                        value=f"**Used:** `{psutil.virtual_memory().percent}%`", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.get_avatar_url())
        await ctx.send(embeds=embed)


def setup(client):
    Stats(client)
