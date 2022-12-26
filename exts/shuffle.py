from math import ceil

import interactions
from interactions import CommandContext
from interactions.ext.lavalink import VoiceClient, VoiceState, Player

import config
from utils.Check import Check


class Shuffle(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    async def shuffle(self, ctx: CommandContext):
        """Shuffle all the songs in the queue"""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        player.shuffle = not player.shuffle
        await ctx.send("🔀 | Shuffle mode " + ("enabled" if player.shuffle else "disabled"))


def setup(client):
    Shuffle(client)
