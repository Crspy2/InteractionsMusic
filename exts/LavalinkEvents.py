import interactions
from interactions.ext.lavalink import VoiceClient, VoiceState, listener, Player
import lavalink
from lavalink import AudioTrack


class LavalinkEvents(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @listener()
    async def on_track_start(self, event: lavalink.TrackStartEvent):
        """
        Fires when track starts
        """
        print("STARTED", event.track)

    @interactions.extension_listener()
    async def on_start(self):
        self.client.lavalink_client.add_node("0.0.0.0", 2333, "youshallnotpass", "us")

    @interactions.extension_listener()
    async def on_voice_state_update(self, before: VoiceState, after: VoiceState):
        """
        Disconnect if bot is alone
        """
        if before and not after.joined:
            voice_states = self.client.get_channel_voice_states(before.channel_id)
            if len(voice_states) == 1 and voice_states[0].user_id == self.client.me.id:
                await self.client.disconnect(before.guild_id)


def setup(client):
    LavalinkEvents(client)
