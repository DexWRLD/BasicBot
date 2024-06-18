import random
import asyncio
import discord
from discord import Embed
import json
import os
from collections import defaultdict
from functools import wraps

COMMANDS = {}
LOOTBOX_CHOICES = [
    "Common Sword", "Common Sword", "Common Sword", "Common Shield", "Common Shield", "Common Shield",  # 30% chance
    "Uncommon Dagger", "Uncommon Dagger", "Uncommon Armor", "Uncommon Armor",  # 20% chance
    "Rare Bow", "Rare Bow",  # 10% chance
    "Rare Helm", "Rare Helm",  # 10% chance
    "Legendary Staff",  # 5% chance
    "Legendary Crown",  # 5% chance
    "Epic Dragon",  # 5% chance
    "Epic Unicorn",  # 5% chance
    "Mythic Phoenix",  # 5% chance
    "Mythic Griffin"  # 5% chance
]

def command(name):
    def decorator(func):
        COMMANDS[name] = func
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@command('help')
def help_command():
    """Returns a help message."""
    help_text = """
    Here are the available commands:
    - `help`: Shows this help message.
    - `dice`: Returns a random number between 1 and 6.
    - `8ball`: Returns a random message.
    - `suggest <your suggestion>`: Records your suggestion.
    - `muteroulette <number>`: Starts a mute roulette game. Guess a number between 1 and 10. If you guess correctly, you will be muted for 5 minutes.
    - `hug <@user>`: Sends a hug to the mentioned user.
    - `?lootbox`: Open a loot box and get a random item.
    - `?inventory`: Show your inventory of items.
    - `rolenamecolor <@role>`: Changes a role's color to a random one.
    - `id <@user>`: Returns the ID of the mentioned user. If no user is mentioned, returns your ID.
    - `servericon`: Displays the server's icon.
    """
    return help_text

@command('dice')
def dice_command():
    """Returns a random number between 1 and 6."""
    return f"your dice number is: {str(random.randint(1, 6))}"

@command('8ball')
def osumball_command():
    """Returns a random message."""
    spisuk = ['Ima shans bratle', 'Nqma shans bratle', 'Ne se znae nishto', 'Ti si baluk, kakvo mislish spored teb', 'Bqgai shmatka', 'Maika ti e muj']
    return random.choice(spisuk)

@command('suggest')
def suggest_command(user: str, suggestion: str) -> str:
    """Records a user's suggestion."""
    with open('suggestions.txt', 'a') as f:
        f.write(f'{user}: {suggestion}\n')
    return f"{user}, your suggestion has been recorded."

@command('muteroulette')
async def mute_roulette_command(message: discord.Message, user: str, number: int) -> None:
    """Starts a mute roulette game."""
    bot_message = await message.channel.send('Starting roulette...')
    await asyncio.sleep(1)
    
    final_number = random.randint(1, 10)
    await bot_message.edit(content=f'Roulette number: {final_number}')
    
    if final_number == number:
        await bot_message.edit(content=f'{user} guessed correctly and is now muted!')
        muted_role = discord.utils.get(message.guild.roles, name="Muted")
        if muted_role:
            await message.author.add_roles(muted_role)
            await asyncio.sleep(5 * 60)  # Wait for 5 minutes
            await message.author.remove_roles(muted_role)
    else:
        await bot_message.edit(content=f'{user} guessed {number}, but the result was {final_number}.')

@command('hug')
def hug_command(user: str, mentioned_user: discord.Member) -> Embed:
    gifs = [
        "https://media1.tenor.com/images/7e30687977c5db417e8424979c0dfa99/tenor.gif",
        "https://media1.tenor.com/images/4d89d7f963b41a416ec8a55230dab31b/tenor.gif",
        "https://media1.tenor.com/images/45b1dd9eaace572a65a305807cfaec9f/tenor.gif",
        "https://media1.tenor.com/images/b4ba20e6cb49d8f8bae81d86e45e4dcc/tenor.gif",
        "https://media1.tenor.com/images/949d3eb3f689fea42258a88fa171d4fc/tenor.gif",
        "https://media1.tenor.com/images/72627a21fc298313f647306e6594553f/tenor.gif",
        "https://media1.tenor.com/images/d3dca2dec335e5707e668b2f9813fde5/tenor.gif",
        "https://media1.tenor.com/images/eee4e709aa896f71d36d24836038ed8a/tenor.gif",
        "https://media1.tenor.com/images/b214bd5730fd2fdfaae989b0e2b5abb8/tenor.gif",
        "https://media1.tenor.com/images/edea458dd2cbc76b17b7973a0c23685c/tenor.gif",
        "https://media1.tenor.com/images/506aa95bbb0a71351bcaa753eaa2a45c/tenor.gif",
        "https://media1.tenor.com/images/42922e87b3ec288b11f59ba7f3cc6393/tenor.gif",
        "https://media1.tenor.com/images/bb841fad2c0e549c38d8ae15f4ef1209/tenor.gif",
        "https://media1.tenor.com/images/234d471b1068bc25d435c607224454c9/tenor.gif",
        "https://media1.tenor.com/images/de06f8f71eb9f7ac2aa363277bb15fee/tenor.gif"
    ]
    embed = Embed(description=f"{user} hugged {mentioned_user.name}!")
    embed.set_image(url=random.choice(gifs))
    return embed

@command('lootbox')
def lootbox_command(user: str) -> str:
    choice = random.choice(LOOTBOX_CHOICES)
    
    # Check if the directory exists, if not, create it
    if not os.path.exists('loot_data'):
        os.makedirs('loot_data')
    
    # Check if the user's file exists, if not, create it and initialize with an empty list
    user_file = f'loot_data/{user}.json'
    if not os.path.exists(user_file):
        with open(user_file, 'w') as f:
            json.dump([], f)
    
    # Load the user's current loot data
    with open(user_file, 'r') as f:
        loot_data = json.load(f)
    
    # Append the new loot to the user's loot data
    loot_data.append(choice)
    
    # Write the updated loot data back to the user's file
    with open(user_file, 'w') as f:
        json.dump(loot_data, f)
    
    return f"CONGRATULATIONS {user}!!, You've opened the server's Loot Box and got `{choice}` !!"

@command('inventory')
def get_inventory(user: str) -> str:
    # Check if the user's file exists, if not, return a message
    user_file = f'loot_data/{user}.json'
    if not os.path.exists(user_file):
        return f"{user}, you have no items in your inventory."

    # Load the user's current loot data
    with open(user_file, 'r') as f:
        loot_data = json.load(f)

    # Categorize the items based on their rarity
    categories = defaultdict(list)
    for item in loot_data:
        rarity = item.split(' ')[0]
        categories[rarity].append(item)

    # Format the inventory message
    inventory_message = f"{user}, here is your inventory:\n"
    for rarity, items in categories.items():
        inventory_message += f"{rarity} items:\n"
        for item in items:
            inventory_message += f"- {item}\n"

    return inventory_message

@command('rolenamecolor')
async def rolenamecolor_command(message: discord.Message, role_mention: str) -> str:
    """Changes a role's color to a random one."""
    # Check if the user has the serverMod role
    if not message.author.guild_permissions.administrator:
        return "You don't have permission to use this command."

    # Extract the role ID from the mention
    role_id = int(role_mention[3:-1].replace("&", "").replace(" ", ""))  # Remove '&' and spaces before converting to int

    # Get the role
    role = discord.utils.get(message.guild.roles, id=role_id)
    if role is None:
        return f"The role `{role_mention}` doesn't exist."

    # Generate a random color
    random_color = discord.Color(random.randint(0, 0xFFFFFF))

    # Change the role's color
    await role.edit(color=random_color)

    return f"The color of the role `{role.name}` has been changed."

@command('id')
def id_command(message: discord.Message, mentioned_user: str = None) -> str:
    """Returns the ID of a user."""
    if isinstance(message, discord.Message):
        if mentioned_user:
            mentioned_user_id = mentioned_user.strip('<@>').split('!')[-1]
            return f"The ID of {mentioned_user} is: {mentioned_user_id}"
        else:
            return f"Your ID is: {message.author.id}"
    else:
        return "Invalid message object. Expected a discord.Message object."

@command('servericon')
async def servericon_command(message: discord.Message) -> str:
    """Displays the server's icon."""
    server = message.guild
    if server.icon:
        return f"Current Server Icon for {server.name}\n{server.icon.url}"
    else:
        return f"The server {server.name} does not have an icon."

async def get_response(user: discord.User, user_input: str, message: discord.Message = None):
    """Returns a response based on the user's input."""
    lowered = user_input.lower().split()
    command = lowered[0]
    args = lowered[1:]
    
    command_func = COMMANDS.get(command)
    if command_func:
        try:
            if asyncio.iscoroutinefunction(command_func):
                if command == 'muteroulette':
                    number = int(args[0])
                    return await command_func(message, user, number)
                elif command == 'hug':
                    mentioned_user = message.mentions[0]
                    return command_func(user, mentioned_user)
                elif command == 'rolenamecolor':
                    role_mention = args[0]
                    return await command_func(message, role_mention)
                elif command == 'servericon':
                    return await command_func(message)
            else:
                if command == 'help' or command == 'dice' or command == '8ball':
                    return command_func()
                elif command == 'suggest':
                    suggestion = ' '.join(args)
                    return command_func(user, suggestion)
                elif command == 'lootbox':
                    return command_func(user)
                elif command == 'inventory':
                    return command_func(user)
                elif command == 'id':
                    mentioned_user = args[0] if args else None
                    return command_func(message, mentioned_user)
        except (TypeError, ValueError) as e:
            return f"Error processing command: {str(e)}"
    else:
        return "Unknown command. Type 'help' to see the available commands."
