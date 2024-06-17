# BasicBot

BasicBot is a versatile and user-friendly Discord bot designed to enhance your server's experience with fun and useful commands.

## Features

- Dice rolls
- 8ball responses
- Suggestion recording
- Interactive games like mute roulette
- Hug command with fun GIFs
- Loot box system with inventory tracking
- Change the color of a mentioned role to a random one (Make sure to move the role above the required roles and to have permissions)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-github-username/BasicBot.git
   ```

2. Navigate to the project directory:
   ```
   cd BasicBot
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Discord token:
   ```
   Discord_Token=YOUR_DISCORD_TOKEN
   ```

## Usage

Run the bot:
```
python main.py
```

## Commands

- `?help`: Shows the help message with all available commands.
- `?dice`: Returns a random number between 1 and 6.
- `?8ball`: Returns a random message.
- `?suggest <your suggestion>`: Records your suggestion.
- `?muteroulette <number>`: Starts a mute roulette game.
- `?hug <@user>`: Sends a hug to the mentioned user.
- `?lootbox`: Open a loot box and get a random item.
- `?inventory`: Show your inventory of items.
- `rolenamecolor <@role>`: Changes a role's color to a random one.

## Contributing

Feel free to open issues or submit pull requests if you have any suggestions or improvements.

## License

This project is licensed under the MIT License.
