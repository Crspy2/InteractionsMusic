from typing import Optional

import interactions
from interactions import Message, CommandContext
from interactions.ext.lavalink import VoiceClient, VoiceState, Player

import config
from utils.Check import Check


class Volume(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_command()
        # name="volume",
        # options=[
        #     interactions.Option(
        #         name="volume",
        #         description="The percentage to change the volume to (min:0, max:200)",
        #         type=interactions.OptionType.INTEGER,
        #         min_values=0,
        #         max_values=200,
        #     )])
    @interactions.option(name="volume", description="The percentage to change the volume to (min:0, max:200)",
                         type=int, min_values=0, max_values=200)
    async def volume(self, ctx: CommandContext, volume: Optional[int] = None) -> Message | None:
        """Change the output volume of the bot!"""
        if not await Check().userInVoiceChannel(ctx): return
        if not await Check().clientInVoiceChannel(ctx): return
        if not await Check().userAndClientInSameVoiceChannel(ctx, self.client): return

        voice: VoiceState = ctx.author.voice
        player: Player
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        if volume is None:
            return await ctx.send(f"The volume is currently set to {volume}%")
        await player.set_volume(volume)
        return await ctx.send(f"The volumed was changed to : `{volume} %`")


def setup(client):
    Volume(client)
