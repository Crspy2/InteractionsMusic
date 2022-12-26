import interactions
import lavalink
from interactions import CommandContext
from interactions.ext.lavalink import VoiceClient, Player, VoiceState

import config
from utils.Check import Check
from utils.sendPlayingSongEmbed import sendPlayingSongEmbed


class NowPlaying(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command(name="now-playing")
    async def nowplaying(self, ctx: CommandContext):
        """Display information on the current song playing"""
        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        if not player.is_playing:
            return await ctx.channel.send(f"{ctx.author.mention} There is currently no song!")

        await sendPlayingSongEmbed(ctx, player.current)


def setup(client):
    NowPlaying(client)