Made to fetch League of Legends, Janna is a Discord bot using Riot Games API.

It consists of three major commands: 

- **/livegame**: If the summoner is currently in a game, it returns the information about this game, including details of other summoners, mode of the game, and who plays what.
- **/profile**: Details of summoner profile, rank, his summoner icon, and pre-migration summoner name.
- **/rotate**: Shows this week's free champion rotation.

### What used:
This project was built using Python and the `discord.py` library.
I used Python because it was a requirement for this project, and after some research, I found out that the most popular Python library to create discord bots is `discord.py`, so I  used that.

### How it was made:
Well, I started this project as a Final Project for Codédex and wanted to do something original and educational. Since I've been playing League of Legends for years, I decided to focus on that. Initially, At first, I wanted only to display profiles and ranks. However, as I explored and tested Riot Games APIs, I realized I could do more.

### What went wrong: 
 Honestly, the most challenging part was the `/livegame` command. I wanted to show summoners by champions with their respective icons inside an embed. Long story short, after some research, I came to find out it is possible only with emojis. So, I had to create and upload 168 emojis in 4 Discord servers. After that, I invited bot to the servers and got emoji ids, stored them in mapping.py. Quite a laborious job, challenging for me. Also, I have no idea how other people are going to use those emojis if they ever use the bot. They probably won't be able to.

### Future improvements:
Some things I have in my todo list:
- Make it so that a player can see their live game when clicking a reaction under the profile embed.
- Allow users to click on players in the live game embed to automatically use the profile command on them. (if possible)
- Bot adaptation to arena mode where 16 players play in 8 teams since it currently only supports 2 teams with 10 players

### What I learned:
 I learned following things during making development of this project:
- Practical experience with classes.
- I learned a lot about the Riot API and how to work with data from APIs.
- I learned using dictionaries for mapping.
- I discovered how switch cases work in Python. Although I didn't use them in my code, I researched it.
- I’ve also learned how to create requests using `aiohttp`.
- Most importantly, I got to know the usage of `discord.py`, its slash commands, customization options for embeds, and how to handle interactions.
