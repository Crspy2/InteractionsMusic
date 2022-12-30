import interactions
from interactions.ext.lavalink import VoiceClient, VoiceState, Player

import config
from utils.Check import Check


class Join(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
    async def join(self, ctx: interactions.CommandContext):
        """Make the bot join the voice channel that you are currently in!"""
        if not await Check().userInVoiceChannel(ctx): return
        if await Check().clientInVoiceChannel(ctx): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect(self_deaf=True)

        await ctx.send(f"{config.SuccessEmoji} **Connected to <#{int(voice.channel_id)}>!**")



def setup(client):
    Join(client)
