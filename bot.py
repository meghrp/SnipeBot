import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='plz')

@bot.command()
async def snipe(ctx, name, message):
    msg = str(message.author) + ": " + str(message.content)
    print(msg)

bot.run(TOKEN)
