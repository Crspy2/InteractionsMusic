import interactions
from interactions import Message, CommandContext, ComponentContext
from interactions.ext.lavalink import VoiceClient, VoiceState, Player

import config
from utils.Check import Check


class Stop(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    async def stop(self, ctx: CommandContext):
        """Make the bot leave the current voice channel!"""
        if not await Check().clientInVoiceChannel(ctx): return
        if not ctx.author.has_permissions(interactions.Permissions.ADMINISTRATOR):
            if not await Check().userInVoiceChannel(ctx): return
            if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        if player.is_playing:
            await player.destroy()
        await self.client.disconnect(ctx.guild.id)

        await ctx.send(f"{config.SuccessEmoji} **Disconnected from <#{player.channel_id}>!**")


def setup(client):
    Stop(client)
