import interactions
from interactions import CommandContext
from interactions.ext.lavalink import VoiceClient, Player, VoiceState

import config
from utils.Check import Check


class Pause(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    async def pause(self, ctx: CommandContext):
        """"Pause/Resume the current track"""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        if not player.paused:
            await player.set_pause(True)
            return await ctx.send(f"**{config.SuccessEmoji} The song has been paused!**")
        await ctx.send(f"**{config.ErrorEmoji} The song is already paused!**")


def setup(client):
    Pause(client)