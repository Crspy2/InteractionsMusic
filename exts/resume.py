import interactions
from interactions import CommandContext
from interactions.ext.lavalink import VoiceClient, Player, VoiceState

import config
from utils.Check import Check


class Resume(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    async def resume(self, ctx: CommandContext):
        """"Resume the current track"""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        if player.paused:
            await player.set_pause(False)
            return await ctx.send(f"{config.SuccessEmoji} The song has been resumed!")
        await ctx.send(f"{config.ErrorEmoji} The current song has not been paused!")


def setup(client):
    Resume(client)