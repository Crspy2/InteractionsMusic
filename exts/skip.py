from math import ceil

import interactions
from interactions import Message, CommandContext
from interactions.ext.lavalink import VoiceClient, VoiceState, Player

import config
from utils.Check import Check


class Skip(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    async def skip(self, ctx: CommandContext):
        """Skip the current song in the queue"""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()


        if not await ctx.author.has_permissions(interactions.Permissions.ADMINISTRATOR)\
                or await ctx.author.has_permissions(interactions.Permissions.MANAGE_GUILD):

            users = []
            userCount = len(users)

            # If user had already skip
            if ctx.author.id in [i[0] for i in users]:
                await ctx.send(
                    f"{config.ErrorEmoji} Waiting for other voice users! (`{userCount}/{ceil(len(self.client.get_channel_voice_states(voice.channel_id)) / 2)}`)")

            # Add to the DB
            userCount += 1

            # Calculate the skipratio
            ratio = userCount / (len(self.client.get_channel_voice_states(voice.channel_id)) - 1) * 100  # It's a percentage
            if not ratio > 50:
                return await ctx.send(
                    f" Waiting for other voice users! (`{userCount}/{ceil(len(self.client.get_channel_voice_states(voice.channel_id)) / 2)}`)")

        # Clean the dict
        await ctx.send(f"{config.SuccessEmoji} Current music skipped!")

        await player.skip()


def setup(client):
    Skip(client)
