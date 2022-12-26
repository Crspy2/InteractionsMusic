import interactions
from interactions import CommandContext
from interactions.ext.lavalink import VoiceClient, Player, VoiceState

import config
from utils.Check import Check


class Restart(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    async def restart(self, ctx: CommandContext):
        """Reload the current song"""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        await player.seek(0)

        await ctx.send(f"{config.SuccessEmoji} **Restarted the current song!**")


def setup(client):
    Restart(client)