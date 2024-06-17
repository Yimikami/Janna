# Janna Discord Bot

## Description
Janna is a Discord bot designed to fetch League of Legends summoner rank information using Riot Games API.

## Features
- **Rank Command**: Fetches and displays the ranked information of a League of Legends summoner.
- **Dynamic Region Handling**: Automatically maps region inputs to Riot API endpoints for various League of Legends regions.
- **Embed Display**: Utilizes Discord embeds to present summoner's rank information in an attractive format.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Yimikami/Janna-bot
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Change .env.example to .env and fill in the required environment variables:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   RIOT_API_KEY=your_riot_api_key
   GUILD_ID=your_discord_guild_id
   ```

## Usage
- Run the bot using:
  ```
  python main.py
  ```
- In Discord, use the `/rank` command followed by the summoner's game name, tagline, and region to fetch their rank information.

## Commands
### `/rank gamename tagline region`
- Fetches and displays the ranked information of the specified summoner in the given region.

## Dependencies
- **Python Libraries**:
  - `discord.py`: For interfacing with Discord API.
  - `aiohttp`: For asynchronous HTTP requests.
  - `python-dotenv`: For loading environment variables from `.env` file.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any improvements or fixes.