import interactions
import lavalink
from interactions import CommandContext, ComponentContext
from interactions.ext.lavalink import Player, VoiceState, VoiceClient
from lavalink import AudioTrack

import config


class Queue(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot

    @interactions.extension_command()
    async def queue(self, ctx: CommandContext | ComponentContext):
        """Display the queue"""
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
        QueueDuration = 0
        for i in range(len(player.queue)):
            QueueDuration += tracks[i].duration.real
            trackDuration = lavalink.format_time(tracks[i].duration.real)
            trackTitle = tracks[i].title.replace("*", "\\*")

            embed.add_field(
                name=f"**{tracks[i].position + 1}: [{trackTitle}]({tracks[i].uri})** (`{trackDuration}`)",
                value=f"Uploaded by: {tracks[i].author}"

            )
        embed.set_footer(f"Total duration: {lavalink.format_time(QueueDuration)} | {len(tracks)} Tracks")
        await ctx.send(embeds=embed)


def setup(client: VoiceClient):
    Queue(client)