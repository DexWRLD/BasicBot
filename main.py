from dotenv import load_dotenv
from discord import Embed, Intents, Client, Message
import discord
from commands import get_response
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
Token = os.getenv('Discord_Token')

intents: Intents=Intents.default()
intents.message_content=True
client:Client = Client(intents=intents)

async def send_message(message: Message, user_message:str) -> None:
    """Sends a message to the Discord channel."""
    if not user_message:
        logging.info('No user message provided.')
        return
    
    if user_message[0]=='?':
        user_message=user_message[1:]
        
    try:
        username = str(message.author)
        response = await get_response(username, user_message, message)
        if isinstance(response, Embed):
            await message.channel.send(embed=response)
        else:
            await message.channel.send(response)
    except Exception as e:
        logging.error(e)

@client.event
async def on_ready() -> None:
    """Logs when the bot is ready."""
    logging.info(f'{client.user} is now running!')

@client.event
async def on_message(message:Message) -> None:
    """Handles incoming messages."""
    if isinstance(message.channel, discord.channel.DMChannel):
        return

    if not message.content.startswith('?'):
        return

    if message.author==client.user:
        return
    
    username:str =str(message.author)
    user_message:str = message.content[1:]
    channel:str =str(message.channel)
    logging.info(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

def main() -> None:
    """Starts the bot."""
    client.run(token=Token)

if __name__=='__main__':
    main()