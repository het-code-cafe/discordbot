import discord
from discord.ext import commands
import requests as r 
import os

PREFIX = "!"
BANNED_WORDS = [
	"pizza hawaii",
	"pizza hawai",
	"scriptie",
	"mark rutte",
	"marc rutte",
	"hugo de jonge"
]

UNFORGIVABLE_WORDS = [
	"lord of the rings was eigenlijk niet zo'n goede film",
	"crucio", 
	"ava kedavra",
	"emacs is beter dan vim"
]

intents = discord.Intents.default()
intents.members = True

# Instantieer bot
# client = discord.Client(intents=intents)
client = commands.Bot(intents=intents, command_prefix=PREFIX)

@client.event
async def on_ready():
	print(f"Logged in as {client.user}")

@client.command()
async def hoi(context):
	await context.message.reply("Hallo!")

@client.command()
async def kat(context):
	req = r.get("https://api.thecatapi.com/v1/images/search")
	res = req.json()
	await context.message.reply(res[0]["url"])

@client.command()
async def koffie(context):
	req = r.get("https://coffee.alexflipnote.dev/random.json")
	res = req.json()
	await context.message.reply(res["file"])

@client.command()
async def testban(context, user: discord.Member):
	if context.message.author.top_role.name == "Moderator":
		await context.message.channel.send("Yeet!")
		await user.ban()
	else: 
		await context.message.reply("UNAUTHORIZED")

@client.command()
async def kanye(context):
	req = r.get("https://api.kanye.rest/")
	res = req.json()
	await context.message.reply(res["quote"])

@client.command()
async def mock(context, *argument):
	arg = "_".join(argument)
	await context.message.reply(f"https://mockingspongebob.org/{arg}.jpg")

@client.command()
async def poke(context, argument):
	msg = ""

	req = r.get(f"https://pokeapi.co/api/v2/pokemon/{argument}")
	res = req.json()

	msg += f"{res['name'].title()}:\n"

	types = res["types"]

	for tp in types:
		msg += f"Type {tp['slot']}: {tp['type']['name'].title()}\n"

	stats = res["stats"]

	for st in stats:
		msg += f"{st['stat']['name'].title()}: {st['base_stat']}\n"

	await context.message.reply(msg)
	
@client.event
async def on_member_join(member):
	guild = member.guild
	if guild.system_channel is not None:
		res = f"Welkom {member.mention} in de {guild.name} server!"
		await guild.system_channel.send(res)

@client.event
async def on_message(message):
	if message.author.id == client.user.id:
		return

	for word in BANNED_WORDS:
		if word in message.content.lower():
			await message.delete()
			await message.channel.send(f"{message.author.mention} je bericht is verwijderd, omdat het een verboden woord bevat.")

	for word in UNFORGIVABLE_WORDS:
		if word in message.content.lower():
			await message.delete()
			await message.channel.send("Yeet!")
			await message.author.ban()
	
	await client.process_commands(message) 
	

	

# Run ik de bot
client.run(os.getenv("TOKEN"))
