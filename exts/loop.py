import interactions
from interactions import CommandContext
from interactions.ext.enhanced import cooldown
from interactions.ext.lavalink import VoiceClient, Player, VoiceState

import config
from utils.Check import Check


class Loop(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command(name="loop-queue")
    @interactions.option(name="loop", description="Enable or disable loop mode for the queue", type=bool, required=True)
    async def loopqueue(self, ctx:CommandContext, loop: bool):
        """Enable or disable the loop queue mode."""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return
        if not await Check().clientIsPlaying(ctx, self.client): return


        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        if loop:
            player.loop = 2
            await ctx.send(f"**{config.SuccessEmoji} The loop mode was enabled for the queue!**")
        else:
            player.loop = 0
            await ctx.send(f"**{config.SuccessEmoji} The loop mode was disabled!**")


    @interactions.extension_command(name="loop-song")
    @interactions.option(name="loop", description="Enable or disable loop mode for the current track", type=bool, required=True)
    async def loopsong(self, ctx: CommandContext, loop: bool):
        """"Enable or disable the loop mode."""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return
        if not await Check().clientIsPlaying(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        if loop:
            player.loop = 1
            await ctx.send(f"{config.SuccessEmoji} The loop mode was enabled for the current track!")
        else:
            player.loop = 0
            await ctx.send(f"{config.SuccessEmoji} The loop mode was disabled!")



def setup(client):
    Loop(client)