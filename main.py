import os
from dotenv import load_dotenv

import aiohttp
import discord
from discord import app_commands, Embed

import mapping

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


class Summoner:
    def __init__(
        self,
        gamename,
        tagline,
        puuid,
        id,
        tier,
        rank,
        lp,
        wins,
        losses,
        icon,
        summonername,
    ):
        self.gamename = gamename
        self.tagline = tagline
        self.puuid = puuid
        self.id = id
        self.tier = tier
        self.rank = rank
        self.lp = lp
        self.wins = wins
        self.losses = losses
        self.icon = icon
        self.summonername = summonername


class RiotAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    async def request(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers={"X-Riot-Token": self.api_key}
            ) as response:
                return await response.json()

    async def get_summoner_by_riot_id(self, gameName, tagLine):
        url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        return await self.request(url)

    async def get_summoner_by_puuid(self, encryptedPUUID, region):
        url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}"
        return await self.request(url)

    async def get_league_by_summoner(self, encryptedSummonerId, region):
        url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}"
        return await self.request(url)

    async def get_match_history(self, encryptedPUUID):
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{encryptedPUUID}/ids?start=0&count=1"
        return await self.request(url)

    async def get_match(self, matchId):
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{matchId}"
        return await self.request(url)

    async def get_summoner_name(self, encryptedPUUID):
        matchId = await self.get_match_history(encryptedPUUID)
        match = await self.get_match(matchId[0])
        for player in match["info"]["participants"]:
            if player["puuid"] == encryptedPUUID:
                return player["summonerName"]

    async def get_live_game(self, encryptedPUUID, region):
        url = f"https://{region}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{encryptedPUUID}"
        return await self.request(url)

    async def findChampionName(self, championId):
        url = (
            f"https://ddragon.leagueoflegends.com/cdn/14.12.1/data/en_US/champion.json"
        )
        champions = await self.request(url)
        champions = champions["data"]
        for champion in champions.values():
            if champion["key"] == str(championId):
                return champion["name"]
            
    async def get_free_champion_rotation(self):
        url = f"https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations"
        return await self.request(url)


getSummoner = RiotAPI(os.getenv("RIOT_API_KEY"))


@tree.command(
    name="profile",
    description="Get the profile of a summoner",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def profile(interaction, gamename: str, region: str):
    tagline = gamename.split("#")[1]
    gamename = gamename.split("#")[0]
    region = region.lower()
    region = mapping.region_mapping.get(region, "euw1")

    summoner = await getSummoner.get_summoner_by_riot_id(gamename, tagline)
    if "status" in summoner:
        await interaction.response.send_message(
            "This summoner does not exist", ephemeral=True
        )
        return

    summoner = await getSummoner.get_summoner_by_puuid(summoner["puuid"], region)
    league = await getSummoner.get_league_by_summoner(summoner["id"], region)
    summonerName = await getSummoner.get_summoner_name(summoner["puuid"])

    summoner = Summoner(
        gamename,
        tagline,
        summoner["puuid"],
        summoner["id"],
        league[0]["tier"],
        league[0]["rank"],
        league[0]["leaguePoints"],
        league[0]["wins"],
        league[0]["losses"],
        summoner["profileIconId"],
        summonerName,
    )

    embed = Embed(
        title=f"{summoner.gamename}#{summoner.tagline}\n{summoner.summonername}",
        description=f"{summoner.tier} {summoner.rank} - {summoner.lp} LP",
        color=0x5CDBF0,
    )
    embed.set_thumbnail(
        url=f"https://ddragon.leagueoflegends.com/cdn/14.12.1/img/profileicon/{summoner.icon}.png"
    )
    embed.add_field(name="Wins", value=summoner.wins, inline=True)
    embed.add_field(name="Losses", value=summoner.losses, inline=True)
    
    await interaction.response.send_message(embed=embed)


@tree.command(
    name="livegame",
    description="Get the live game of a summoner",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def livegame(interaction, gamename: str, region: str):
    tagline = gamename.split("#")[1]
    gamename = gamename.split("#")[0]
    region = region.lower()
    region = mapping.region_mapping.get(region, "euw1")

    summoner = await getSummoner.get_summoner_by_riot_id(gamename, tagline)
    if "status" in summoner:
        await interaction.response.send_message(
            "This summoner does not exist", ephemeral=True
        )
        return

    live_game = await getSummoner.get_live_game(summoner["puuid"], region)
    if "status" in live_game:
        await interaction.response.send_message(
            "This summoner is not in a live game", ephemeral=True
        )
        return
    
    participants = live_game["participants"]
    blue_team = []
    red_team = []
    for player in participants:
        if player["teamId"] == 100:
            blue_team.append(player)
        else:
            red_team.append(player)
    gameQueue = live_game["gameQueueConfigId"]
    gameQueue = mapping.queue_mapping.get(gameQueue, "Unknown")
    embed = Embed(
        title=f"{gamename}#{tagline}'s Live Game",
        description=f"Gamemode: {gameQueue}\nGame Time: {round((live_game['gameLength'] / 60))} minutes",
        color=0x5CDBF0,
    )
    blue_team_string = ""
    red_team_string = ""
    line_string = ""
    for player in blue_team:
        blue_team_string += f"{mapping.emoji_mapping.get(str(player['championId']))}{await getSummoner.findChampionName(player['championId'])} - {player['riotId']}\n"
    for player in red_team:
        red_team_string += f"{mapping.emoji_mapping.get(str(player['championId']))}{await getSummoner.findChampionName(player['championId'])} - {player['riotId']}\n"
    embed.add_field(name="Blue Team", value=blue_team_string, inline=True)
    for _ in range(5):
        line_string += "|\n"
    embed.add_field(name="|", value=line_string, inline=True)
    embed.add_field(name="Red Team", value=red_team_string, inline=True)
    
    await interaction.response.send_message(embed=embed)

@tree.command(name="rotation", description="Get the free champion rotation", guild=discord.Object(id=os.getenv("GUILD_ID")))
async def rotation(interaction):
    rotation = await getSummoner.get_free_champion_rotation()
    free_champions = rotation["freeChampionIds"]
    low_level_free_champions = rotation["freeChampionIdsForNewPlayers"]
    free_champions_string = ""
    low_level_free_champions_string = ""
    for champion in free_champions:
        free_champions_string += f"{mapping.emoji_mapping.get(str(champion))}{await getSummoner.findChampionName(champion)}\n"
    for champion in low_level_free_champions:
        low_level_free_champions_string += f"{mapping.emoji_mapping.get(str(champion))}{await getSummoner.findChampionName(champion)}\n"
    embed = Embed(
        title="Free Champion Rotation",
        color=0x5CDBF0,
    )
    embed.add_field(name="Free Champions", value=free_champions_string, inline=True)
    embed.add_field(name="Low Level Free Champions (1-10)", value=low_level_free_champions_string, inline=True)
    
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print(f"{client.user.name} has connected to Discord!")

client.run(os.getenv("DISCORD_TOKEN"))
