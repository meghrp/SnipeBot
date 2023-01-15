import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=[
                   'pls ', 'plz ', 'Plz ', 'Pls '], intents=discord.Intents.all(), help_command=None)
bot.sniped_messages = {}
bot.edit_messages = {}
teal = discord.Colour.from_rgb(0, 100, 100)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_guild_join(guild):
    print(f"Joined {guild.name}")
    owner = await bot.application_info()
    owner = owner.owner
    await owner.send(f"Joined {guild.name} ({guild.id})")


async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except discord.errors.Forbidden:
        try:
            await ctx.send("I can't send embeds. Please give me the permission to do so.")
        except discord.errors.Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue?", embed=embed)


@bot.event
async def on_message_delete(message):
    if message.attachments:
        bot.sniped_messages[message.guild.id] = (
            message.content, message.author, message.channel.name, message.created_at, message.attachments[0].proxy_url)
    else:
        bot.sniped_messages[message.guild.id] = (
            message.content, message.author, message.channel.name, message.created_at)


@bot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        bot.edit_messages[before.guild.id] = (
            before.content, after.content, before.author, before.channel.name, before.created_at)


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
            embed = discord.Embed(description=content,
                                  color=teal, timestamp=created_at)
            if is_img:
                embed.set_image(url=img_url)
            embed.set_author(name=f"{author.name}", icon_url=author.avatar)
            embed.set_footer(text=f"#{channel}")
            await send_embed(ctx, embed)
    except KeyError:
        await ctx.send("Nothing to snipe")


@bot.command()
async def editsnipe(ctx):
    try:
        content_before, content_after, author, channel, created_at = bot.edit_messages[
            ctx.guild.id]
        if author.id != bot.user.id:
            embed = discord.Embed(description=content_before,
                                  color=teal, timestamp=created_at)
            embed.set_author(name=f"{author.name}", icon_url=author.avatar)
            embed.set_footer(text=f"#{channel}")
            await send_embed(ctx, embed)
    except KeyError:
        await ctx.send("Nothing to snipe")


@bot.command()
@commands.is_owner()
async def servers(ctx):
    try:
        for i in bot.guilds:
            await ctx.author.send(f"{i.name} ({i.id})")
    except:
        pass


@bot.command()
@commands.is_owner()
async def leave(ctx, guild_id=None):
    if guild_id is None:
        guild = ctx.guild
    else:
        guild = bot.get_guild(int(guild_id))
    try:
        await guild.leave()
        print(f"Left {guild.name}")
    except:
        await ctx.send("Invalid guild id")


@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')


@bot.command()
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=975891582354079773&permissions=84992&scope=bot")


@bot.command()
async def github(ctx):
    await ctx.send("https://github.com/meghrp/SnipeBot")


@bot.command()
async def prefix(ctx):
    await ctx.send("`pls `, `plz `, `Pls `, `Plz `")


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Info", description="Bot info", color=teal)
    embed.add_field(name="Author", value="mehg#6129")
    embed.add_field(name="Library", value="discord.py")
    embed.add_field(name="Servers", value=f"{len(bot.guilds)}")
    embed.add_field(name="Users", value=f"{len(bot.users)}")
    embed.add_field(name="Ping", value=f"{round(bot.latency * 1000)}ms")
    embed.set_thumbnail(url=bot.user.avatar)
    await send_embed(ctx, embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Help", description="Help for the bot", color=teal)
    embed.add_field(name="ping", value="Shows the bot's ping")
    embed.add_field(name="info", value="Shows info about the bot")
    embed.add_field(name="invite", value="Sends the bot's invite link")
    embed.add_field(name="github", value="Sends the bot's github link")
    embed.add_field(name="prefix", value="Shows the bot's prefix")
    embed.add_field(name="help", value="Shows this message")
    embed.set_thumbnail(url=bot.user.avatar)
    await send_embed(ctx, embed)


bot.run(TOKEN)
