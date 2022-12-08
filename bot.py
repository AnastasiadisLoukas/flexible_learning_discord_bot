import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="r!", intents=discord.Intents.all())
client= discord.Client()
bot.load_extension("databasesetup")
bot.load_extension("somecommands")
bot.load_extension("contacts")
bot.load_extension("moderation")
bot.load_extension("testcommands")
bot.load_extension("agentchatcommands")
bot.load_extension('reactionroles')
bot.load_extension("utility")
bot.run("Your bot token here ")



