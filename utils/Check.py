from interactions import CommandContext, ComponentContext
from interactions.ext.lavalink import VoiceClient, Player, VoiceState

import config


class Check:
    async def userInVoiceChannel(self, ctx: CommandContext | ComponentContext) -> bool:
        """Check if the user is in a voice channel"""
        if ctx.author.voice:
            return True
        await ctx.send(f"{config.ErrorEmoji} You are not connected to a voice channel!", ephemeral=True)
        return False

    async def clientInVoiceChannel(self, ctx: CommandContext | ComponentContext) -> bool:
        """Check if the client is in a voice channel"""
        player: Player  # Typehint player variable to see their methods
        if (player := ctx.guild.player) is None:
            await ctx.send(f"{config.ErrorEmoji} I'm not connected to a voice channel!", ephemeral=True)
            return False
        return True

    async def clientNotInVoiceChannel(self, ctx: CommandContext | ComponentContext) -> bool:
        """Check if the client is not in a voice channel"""
        player: Player  # Typehint player variable to see their methods
        if (player := ctx.guild.player) is not None:
            await ctx.send(f"{config.ErrorEmoji} I'm already connected to a voice channel!", ephemeral=True)
            return False
        return True

    async def userAndClientInSameVoiceChannel(self, ctx: CommandContext | ComponentContext, client: VoiceClient) -> bool:
        """Check if the user and the client are in the same voice channel"""

        voice: VoiceState = ctx.author.voice
        voice_states = client.get_channel_voice_states(voice.channel_id)

        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        if player.is_connected:
            botState = False
            authorState = False
            for state in voice_states:
                if state.user_id == client.me.id:
                    botState = True
                if state.user_id == ctx.author.id:
                    authorState = True

            if botState and authorState:
                return True
            await ctx.send(f"{config.ErrorEmoji} You are not in the same voice channel as me!", ephemeral=True)
            return False
        else:
            return True


    async def clientIsPlaying(self, ctx: CommandContext | ComponentContext, client: VoiceClient) -> bool:
        """Check if the client is playing"""
        player: Player = client.lavalink_client.player_manager.get(int(ctx.guild.id))

        if player.is_playing:
            return True
        await ctx.send(f"{config.ErrorEmoji} There is currently no song to replay!", ephemeral=True)
        return False
