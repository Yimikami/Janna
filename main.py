import os
from dotenv import load_dotenv
import aiohttp

import discord
from discord import app_commands, Embed


load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


class Summoner:
    def __init__(
        self, gamename, tagline, puuid, id, tier, rank, lp, wins, losses, icon
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


class RiotAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    async def get_summoner_by_riot_id(self, gameName, tagLine):
        url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        response = await self.request(url)
        return response

    async def get_summoner_by_puuid(self, encryptedPUUID, region):
        url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}"
        response = await self.request(url)
        return response

    async def get_league_by_summoner(self, encryptedSummonerId, region):
        url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}"
        response = await self.request(url)
        return response

    async def get_profile_icon(self, iconId):
        url = f"https://ddragon.leagueoflegends.com/cdn/14.12.1/img/profileicon/{iconId}.png"
        response = await self.request(url)
        return response

    async def request(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers={"X-Riot-Token": self.api_key}
            ) as response:
                return await response.json()


getSummoner = RiotAPI(os.getenv("RIOT_API_KEY"))


@tree.command(
    name="rank",
    description="Get the rank of a summoner",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def rank(interaction, gamename: str, tagline: str, region: str):
    region = region.upper()
    match region:
        case "EUW":
            region = "euw1"
        case "EUNE":
            region = "eun1"
        case "NA":
            region = "na1"
        case "KR":
            region = "kr"
        case "JP":
            region = "jp1"
        case "BR":
            region = "br1"
        case "LAN":
            region = "la1"
        case "LAS":
            region = "la2"
        case "OCE":
            region = "oc1"
        case "TR":
            region = "tr1"
        case "RU":
            region = "ru"
        case "PBE":
            region = "pbe1"
        case _:
            region = "euw1"

    summoner = await getSummoner.get_summoner_by_riot_id(gamename, tagline)
    summoner = await getSummoner.get_summoner_by_puuid(summoner["puuid"], region)
    league = await getSummoner.get_league_by_summoner(summoner["id"], region)
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
    )

    embed = Embed(
        title=f"{summoner.gamename}#{summoner.tagline}",
        description=f"{summoner.tier} {summoner.rank} - {summoner.lp} LP",
        color=0x5CDBF0,
    )
    embed.set_thumbnail(
        url=f"https://ddragon.leagueoflegends.com/cdn/14.12.1/img/profileicon/{summoner.icon}.png"
    )
    embed.add_field(name="Wins", value=summoner.wins, inline=True)
    embed.add_field(name="Losses", value=summoner.losses, inline=True)
    await interaction.response.send_message(embed=embed)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print(f"{client.user.name} has connected to Discord!")


client.run(os.getenv("DISCORD_TOKEN"))
