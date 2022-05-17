import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='plz ')
bot.sniped_messages = {}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@bot.command()
async def snipe(ctx):
    content, author, channel, created_at = bot.sniped_messages[ctx.guild.id]
    embed = discord.Embed(description=content, color=discord.Color.teal(), timestamp=created_at)
    embed.set_author(name=f"{author.name}", icon_url=author.avatar_url)
    embed.set_footer(text=f"#{channel}")
    await ctx.send(embed=embed)

bot.run(TOKEN)
