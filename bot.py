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
    if message.attachments:
        bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at, message.attachments[0].proxy_url)
    else:
        bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@bot.command()
async def snipe(ctx):
    try:
        is_img = None
        try:
            content, author, channel, created_at, img_url = bot.sniped_messages[ctx.guild.id]
            is_img = True
        except:
            content, author, channel, created_at = bot.sniped_messages[ctx.guild.id]
        if author.id != bot.user.id:
            embed = discord.Embed(description=content, color=discord.Color.teal(), timestamp=created_at)
            if is_img:
                embed.set_image(url=img_url)
            embed.set_author(name=f"{author.name}", icon_url=author.avatar_url)
            embed.set_footer(text=f"#{channel}")
            await ctx.send(embed=embed)
    except KeyError:
        await ctx.send("Nothing to snipe")

@bot.command()
@commands.is_owner()
async def servers(ctx):
    try:
        for i in bot.guilds:
            await ctx.send(i.name)
    except:
        pass

bot.run(TOKEN)
