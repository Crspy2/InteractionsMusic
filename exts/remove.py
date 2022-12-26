import interactions
import lavalink
from interactions import CommandContext
from interactions.ext.lavalink import VoiceClient, Player, VoiceState

import config
from utils.Check import Check


class Remove(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
        # options=[
            # interactions.Option(
            #     name="index",
            #     description="The index of the queued song to remove",
            #     type=interactions.OptionType.INTEGER,
            #     min_values=0,
            #     required=True,
            # )])
    @interactions.option(name="index",description="The index of the queued song to remove", type=int,
                         min_values=0, required=True)
    async def remove(self, ctx: CommandContext, index: int):
        """Remove a song by its index in the queue"""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        tracks = player.queue

        if (int(index) - 1) > len(tracks):
            return await ctx.send(f"{config.ErrorEmoji} The provided index is invalid!")

        if tracks == 0:
            return await ctx.send(f"{config.ErrorEmoji} The queue is empty!")

        index = int(index)

        # Remove
        player.delete(index)

        track = tracks[index - 2]
        trackDuration = lavalink.format_time(track.duration.real)
        trackTitle = track.title.replace("*", "\\*")
        trackUrl = track.uri

        await ctx.send(f"Song removed : **[{trackTitle}]({trackUrl})** ({trackDuration})")


def setup(client):
    Remove(client)