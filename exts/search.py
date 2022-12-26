import interactions
import lavalink
from interactions import CommandContext
from interactions.ext.lavalink import VoiceClient, Player, VoiceState

import config
from exts.play import noResultFound
from utils.Check import Check


class Search(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    @interactions.option(name="query", description="the song to search Youtube for", type=str, required=True)
    async def search(self, ctx: CommandContext, query: str):
        """Clear the queue"""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        msg = await ctx.send(f"{config.YouTubeLogo} Searching {config.LoadingEmoji}")

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        tracks = await player.search_youtube(query)

        message = ""
        number = 0
        if tracks is None:
            await noResultFound(msg)
            return None
        for i in tracks:
            if number >= 8:
                break
            number += 1
            duration = lavalink.format_time(i.duration.real)
            message += f"**{number}) [{i.title}]({i.uri}])** (`{duration}`)\n"
        embed = interactions.Embed(title="Search results :",
                                   description=f"choose the number that corresponds to the music.\nWrite `0` to pass the cooldown.\n\n{message}",
                                   color=config.EMBEDCOLOR)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.get_avatar_url())
        await msg.edit(embeds=embed)


def setup(client):
    Search(client)
