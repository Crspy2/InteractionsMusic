from math import ceil

import interactions
import lavalink
from interactions import Message, CommandContext, ComponentContext
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

        stop_button = interactions.Button(
            style=interactions.ButtonStyle.DANGER,
            label="stop",
            custom_id="stop"
        )
        skip_button = interactions.Button(
            style=interactions.ButtonStyle.SECONDARY,
            label="skip",
            custom_id="skip"
        )

        queue_button = interactions.Button(
            style=interactions.ButtonStyle.SUCCESS,
            label="queue",
            custom_id="queue"
        )

        pauseresume_button = interactions.Button(
            style=interactions.ButtonStyle.PRIMARY,
            label="pause/resume",
            custom_id="pause/resume"
        )

        row = interactions.ActionRow(
            components=[stop_button, skip_button, queue_button, pauseresume_button]
        )

        await ctx.send(
            content=f"{config.MusicEmoji} Now Playing **{player.current.title}** (`{lavalink.format_time(player.current.duration.real)}`)",
            components=row)

        await player.skip()

    @interactions.extension_component("stop")
    async def stop_button(self, ctx: ComponentContext):
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

    @interactions.extension_component("skip")
    async def skip_button(self, ctx: ComponentContext):
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        if not await ctx.author.has_permissions(interactions.Permissions.ADMINISTRATOR) \
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
            ratio = userCount / (
                    len(self.client.get_channel_voice_states(voice.channel_id)) - 1) * 100  # It's a percentage
            if not ratio > 50:
                return await ctx.send(
                    f" Waiting for other voice users! (`{userCount}/{ceil(len(self.client.get_channel_voice_states(voice.channel_id)) / 2)}`)")

        # Clean the dict
        await ctx.send(f"{config.SuccessEmoji} Current music skipped!")

        await player.skip()

    @interactions.extension_component("queue")
    async def queue_button(self, ctx: ComponentContext):
        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        tracks = player.queue

        if len(tracks) == 0:
            return await ctx.send(f"{config.ErrorEmoji} The queue is empty!")

        embed = interactions.Embed(
            title="**Queue**",
            description="The current songs in the queue are:",
            color=config.EMBEDCOLOR
        )

        for i in range(len(player.queue)):
            trackDuration = lavalink.format_time(tracks[i].duration.real)
            trackTitle = tracks[i].title.replace("*", "\\*")

            embed.add_field(
                name=f"**{tracks[i].position}: [{trackTitle}]({tracks[i].uri})** (`{trackDuration}`)",
                value=f"Uploaded by: {tracks[i].author}"
            )

        await ctx.send(embeds=embed)

    @interactions.extension_component("pause/resume")
    async def pause_button(self, ctx: ComponentContext):
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
        elif player.paused:
            await player.set_pause(False)
            return await ctx.send(f"**{config.SuccessEmoji} The song has been resumed!**")


def setup(client):
    Skip(client)
