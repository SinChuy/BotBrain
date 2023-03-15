import os
import openai
from twitchio.ext import commands

# Set up OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Define the bot class
class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=os.environ['TMI_TOKEN'],
                         client_id=os.environ['CLIENT_ID'],
                         nick=os.environ['BOT_NICK'],
                         prefix=os.environ['BOT_PREFIX'],
                         initial_channels=[os.environ['CHANNEL_NAME']])

    async def event_ready(self):
        print(f'{os.environ["BOT_NICK"]} has connected to Twitch!')

    async def event_message(self, message):
        # Ignore messages from the bot itself
        if message.author.name.lower() == os.environ['BOT_NICK'].lower():
            return

        # Process commands
        await self.handle_commands(message)

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

# Function to connect to Twitch
def connect_twitch_bot():
    bot = TwitchBot()
    bot.run()

if __name__ == "__main__":
    connect_twitch_bot()
