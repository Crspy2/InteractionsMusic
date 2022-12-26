import interactions
import lavalink
from interactions import CommandContext
from interactions.ext.lavalink import VoiceState, Player
from lavalink import AudioTrack

import config


async def sendPlayingSongEmbed(ctx: CommandContext, track: AudioTrack):
    voice: VoiceState = ctx.author.voice
    player: Player
    if (player := ctx.guild.player) is None:
        player = await voice.connect()

    volume = player.volume

    # Track duration
    trackDuration = lavalink.format_time(track.duration.real)

    # Queue size and duration
    queueSize = len(player.queue)
    queueDur = 0
    for track in player.queue:
        queueDur += track.duration.real

    # Title
    trackTitle = track.title.replace("*", "\\*")

    # Loop and LoopQueue
    if player.loop == 1:
        isLoop = "1"
        isLoopQueue = "0"
    elif player.loop == 2:
        isLoop = "0"
        isLoopQueue = "1"
    else:
        isLoop = "0"
        isLoopQueue = "0"

    # Embed
    embed = interactions.Embed(
        title="Playing Song:",
        description=f"**[{trackTitle}]({track.uri})**",
        color=config.EMBEDCOLOR
    )

    if track.identifier:
        embed.set_thumbnail(url=f"https://img.youtube.com/vi/{track.identifier}/default.jpg")
    embed.add_field(
        name="Requested by :",
        value=f"`{track.requester}`"
    )
    embed.add_field(
        name="Duration :",
        value=f"`{trackDuration}`"
    )
    embed.add_field(
        name="Volume :",
        value=f"`{volume}%`"
    )
    embed.add_field(
        name="Loop song:",
        value=isLoop.replace("1", f"{config.SuccessEmoji}")
        .replace("0", f"{config.ErrorEmoji}")
    )
    embed.add_field(
        name="Loop queue:",
        value=isLoopQueue.replace("1", f"{config.SuccessEmoji}")
        .replace("0", f"{config.ErrorEmoji}")
    )
    embed.add_field(
        name="Lyrics :",
        value=f"`/lyrics`"
    )
    embed.add_field(
        name="Queue :",
        value=f"`{queueSize} song(s) ({lavalink.format_time(queueDur)})`",
    )
    embed.add_field(
        name="DJ Role :",
        value=f"`@role`"
    )
    await ctx.send(embeds=embed)
