import aiohttp
import interactions
import lavalink
from interactions import CommandContext, Message
from interactions.ext.lavalink import VoiceClient, VoiceState, Player
import tekore
from lavalink import AudioTrack
from youtubesearchpython import PlaylistsSearch

import config
from utils.Check import Check


async def searchSpotifyTrack(self, ctx: CommandContext, msg: Message, args: str) -> AudioTrack | None:
    """Get a YouTube link from a Spotify link."""
    voice: VoiceState = ctx.author.voice
    player: Player
    if (player := ctx.guild.player) is None:
        player = await voice.connect()

    # Get track's id
    trackId = tekore.from_url(args)
    try:
        track = await self.client.spotify.track(trackId[1])
    except:
        await msg.edit(f"{config.ErrorEmoji} The Spotify link is invalid!")
        return None
    title = track.name
    artist = track.artists[0].name

    # Search on youtube
    track = await player.search_youtube(f"{title} {artist}")
    if len(track) == 0:
        await noResultFound(msg)
        return None
    return track[0]


async def searchSpotifyPlaylist(self, ctx: CommandContext, msg: Message, args: str) -> list[AudioTrack] | None:
    """Get Spotify links from a playlist link."""
    voice: VoiceState = ctx.author.voice
    player: Player
    if (player := ctx.guild.player) is None:
        player = await voice.connect()

    # Get palylist's id
    playlistId = tekore.from_url(args)
    try:
        playlist = await self.client.spotify.playlist(playlistId[1])
    except:
        await msg.edit(f"{config.ErrorEmoji} The Spotify playlist is invalid!")
        return None

    trackLinks = []
    if 20 != 0 and playlist.tracks.total > 20:
        await playlistTooLarge(msg)
        return None
    await msg.edit(f"{config.SpotifyLogo} Loading{config.LoadingEmoji} [`{args}`]")

    for i in playlist.tracks.items:
        title = i.track.name
        artist = i.track.artists[0].name

        # Search on youtube
        track = await player.search_youtube(f"{title} {artist}")
        if track is None:
            await msg.edit(f"{config.ErrorEmoji} No song found for : `{title} - {artist}` !")
        else:
            trackLinks.append(track[0])
    if not trackLinks:  # if len(trackLinks) == 0:
        return None
    return trackLinks


async def searchDeezer(ctx: CommandContext, msg: Message, args: str) -> None | AudioTrack | list[AudioTrack]:
    """Get a YouTube link from a Deezer link."""
    async with aiohttp.ClientSession() as session:
        async with session.get(args) as response:
            # Chack if it's a track
            if "track" in response._real_url.path:
                link = await searchDeezerTrack(ctx, session, response)
                if link is None:
                    return None
                return link
            if "playlist" in response._real_url.path:
                links = await searchDeezerPlaylist(ctx, session, response)
                if links is None:
                    return None
                return links
            await msg.edit(f"{config.ErrorEmoji} The Deezer link is not a track!")
            return None


async def searchDeezerTrack(ctx: CommandContext, msg: Message, session, response) -> AudioTrack | None:
    # Get the music ID
    trackId = response._real_url.name
    async with session.get(f"https://api.deezer.com/track/{trackId}") as response:
        response = await response.json()
        title = response["title_short"]
        artist = response["artist"]["name"]

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        # Search on youtube
        track = await player.search_youtube(f"{title} {artist}")
        if len(track) == 0:
            await noResultFound(msg)
            return None
        return track[0]


async def searchDeezerPlaylist(ctx: CommandContext, msg: Message, session, response) -> list[AudioTrack] | None:
    # Get the playlist ID
    playlistId = response._real_url.name
    async with session.get(f"https://api.deezer.com/playlist/{playlistId}") as response:
        response = await response.json()
        if 20 != 0 and response["nb_tracks"] > 20:
            await playlistTooLarge(msg)
            return None
        await msg.edit(
            f"{config.DeezerLogo} Loading{config.LoadingEmoji}")
        trackLinks = []

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        for i in response["tracks"]["data"]:
            title = i["title_short"]
            artist = i["artist"]["name"]
            # Search on youtube
            track = player.search_youtube(f"{title} {artist}")
            if track == 0:
                await msg.edit(
                    f"{config.ErrorEmoji} No song found for : `{title} - {artist}` !")
            else:
                trackLinks.append(track[0])
        if not trackLinks:
            return None
        return trackLinks


async def searchSoundcloud(ctx: CommandContext, msg: Message, args: str) -> None | list[AudioTrack] | AudioTrack:
    """Get a YouTube link from a SoundCloud link."""
    voice: VoiceState = ctx.author.voice
    player: Player
    if (player := ctx.guild.player) is None:
        player = await voice.connect()

    track = await player.search_soundcloud(args)

    if len(track) == 0:
        await noResultFound(msg)
        return None

    elif len(track) > 1:
        if 20 != 0 and len(track) > 20:
            await playlistTooLarge(msg)
            return None
        return track

    return track[0]


async def searchQuery(ctx: CommandContext, args: str) -> AudioTrack:
    """Get a YouTube link from a query."""
    voice: VoiceState = ctx.author.voice
    player: Player
    if (player := ctx.guild.player) is None:
        player = await voice.connect()

    track = await player.search_youtube(args)
    return track[0]


async def searchPlaylist(ctx: CommandContext, msg: Message, args) -> list[AudioTrack] | None:
    """Get YouTube links from a playlist link."""
    videoCount = int(PlaylistsSearch(args, limit=1).result()["result"][0])
    if videoCount == 0:
        await noResultFound(msg)
        return None
    if videoCount > 20:
        await playlistTooLarge(msg)
        return None
    await msg.edit(f"{config.YouTubeLogo} Loading{config.LoadingEmoji}")

    voice: VoiceState = ctx.author.voice
    player: Player
    if (player := ctx.guild.player) is None:
        player = await voice.connect()

    tracks = await player.search_youtube(args)
    return tracks


async def playlistTooLarge(msg: Message) -> None:
    await msg.edit(f"{config.ErrorEmoji} The playlist is too big! (max : 20 tracks)")


async def noResultFound(msg: Message) -> None:
    await msg.edit(f"{config.ErrorEmoji} No result found!")


class Play(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    @interactions.option(name="query", description="The song/url to play", type=str, required=True)
    async def play(self, ctx: interactions.CommandContext, query: str) -> Message | None:
        """Play music from YouTube, Spotify, Soundcloud or other audio providers!"""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        # Spotify
        if query.startswith("https://open.spotify.com"):
            msg: Message = await ctx.send(f"{config.SpotifyLogo} Searching {config.LoadingEmoji} [`{query}`]")
            if query.startswith("https://open.spotify.com/track"):
                args = await searchSpotifyTrack(self, ctx, msg, query)
            elif query.startswith("https://open.spotify.com/playlist"):
                args = await searchSpotifyPlaylist(self, ctx, msg, query)
            else:
                return await ctx.send(
                    f"{config.ErrorEmoji} **Only Spotify playlist and Spotify track are available!**")
            if args is None:
                return

        # Deezer
        elif query.startswith("https://deezer.page.link") or query.startswith("https://www.deezer.com"):
            msg: Message = await ctx.send(f"{config.DeezerLogo} Searching {config.LoadingEmoji} [`{query}`]")
            args = await searchDeezer(ctx, msg, query)
            if args is None:
                return

        # SoundCloud
        elif query.startswith("https://soundcloud.com"):
            msg: Message = await ctx.send(f"{config.SoundCloudLogo} Searching {config.LoadingEmoji} [`{query}`]")
            args = await searchSoundcloud(ctx, msg, query)
            if args is None:
                return

        # Youtube Playlist
        elif query.startswith("https://www.youtube.com/playlist"):
            msg: Message = await ctx.send(f"{config.YouTubeLogo} Searching {config.LoadingEmoji} [`{query}`]")
            args = await searchPlaylist(ctx, msg, query)
            if args is None:
                return

        # YouTube video
        elif query.startswith("https://www.youtube.com/watch"):
            msg = await ctx.send(f"{config.YouTubeLogo} Searching {config.LoadingEmoji} [`{query}`]")
            # Check if the link exists
            voice: VoiceState = ctx.author.voice
            player: Player
            if (player := ctx.guild.player) is None:
                player = await voice.connect()

            track = await player.search_youtube(query)
            args = track[0]
            if track is None:
                return await msg.edit(f"{config.ErrorEmoji} The YouTube link is invalid!")

        # Query
        else:
            msg = await ctx.send(f"{config.YouTubeLogo} Searching {config.LoadingEmoji} [`{query}`]")
            args = await searchQuery(ctx, query)
            if args is None:
                return

        track = args

        # NOTE: ctx.author.voice can be None if you ran a bot after joining the voice channel
        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        player.add(track, int(ctx.author.id))

        if player.is_playing:
            return await msg.edit(
                f"{config.SuccessEmoji} Added **{track.title}** (`{lavalink.format_time(track.duration.real)}`) to the queue")
        await player.play()
        return await msg.edit(
            f"{config.MusicEmoji} Now Playing **{track.title}** (`{lavalink.format_time(track.duration.real)}`)")


def setup(client):
    Play(client)
