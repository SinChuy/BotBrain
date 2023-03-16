import os
import openai
from twitchio.ext import commands
import requests

# Set up OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

token1 = os.environ['TMI_TOKEN']


# Define the bot class
class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(token=os.environ['TMI_TOKEN'],
                         client_id=os.environ['CLIENT_ID'],
                         nick=os.environ['BOT_NICK'],
                         prefix=os.environ['BOT_PREFIX'],
                         initial_channels=[os.environ['CHANNEL_NAME']])

        self.loop.run_until_complete(self.start())
    
    @commands.command(name='ask')
    async def ask_command(self, ctx, *, question):
        # Generate a response using ChatGPT
        response = self.get_chatgpt_response(question)
        await ctx.send(response)

    def get_chatgpt_response(self, prompt):
        model_engine = "text-davinci-002"  # Replace with the desired model engine
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=50,  # Limit the response length
            n=1,
            stop=None,
            temperature=0.5,  # Adjust the randomness of the response
            top_p=1,
        )

        return response.choices[0].text.strip()
    
    async def send_message(self, message):
        channel = self.get_channel(os.environ['CHANNEL_NAME'])
        await channel.send(message)
        
    async def event_ready(self):
        print(f'{os.environ["BOT_NICK"]} has connected to Twitch!')
    
    async def create_clip(self, client_id, oauth_token, broadcaster_id):
        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {oauth_token}"
        }
        url = f"https://api.twitch.tv/helix/clips?broadcaster_id={broadcaster_id}"
        response = requests.post(url, headers=headers)

        if response.status_code == 202:
            clip_data = response.json()
            return clip_data["data"][0]["edit_url"]
        else:
            return None
        
    async def event_message(self, message):
        # Ignore messages from the bot itself
        clip_url = ""
        if message.author.name == os.environ['BOT_NICK'].lower():
            return
        
        if message.content.lower() == "!clip":
            clip_url = await self.create_clip(os.environ['CLIENT_ID'], os.environ['TMI_TOKEN'], "217378869")
            if clip_url:
                await message.channel.send(f"Here's a clip of the stream: {clip_url}")
            else:
                await message.channel.send("Failed to create a clip. Please try again later.")
            # Process commands

        await self.handle_commands(message)

  