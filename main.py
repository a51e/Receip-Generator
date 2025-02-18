import json
import discord
import os
from pystyle import Colors
from discord.ext import commands


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

config = json.load(open("config.json", encoding="utf-8"))


async def load_cogs():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')


def activity_name(config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("activity", "Cooking")  # Standardname, falls nicht vorhanden
    except FileNotFoundError:
        return "Cooking"  # Standardname, falls Datei nicht existiert
    

@bot.event
async def on_ready():
    activity1 = activity_name()

    activity = discord.Activity(
        name=activity1,
        type=discord.ActivityType.competing 
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await load_cogs()
    await bot.tree.sync()


    print(f"\n\nWe have logged in as {bot.user} | In {len(bot.guilds)} Servers:")
    for guild in bot.guilds:
        print(Colors.cyan + guild.name + Colors.reset) 



@bot.event
async def on_message(message):


    if message.author == bot.user:
            return
    
    msg_content = message.content.lower()

    if "how" in msg_content and "generate" in msg_content:
        await message.reply("Check out <#1335030021655494766> to see how you can generate!")
    elif "difference" in msg_content and "spoofed" in msg_content:
        await message.reply("Spoofed emails are sending with the brand email domains (noreply@stockx.com) and normal email is sent from our domain (noreply@maisonreceipts.cc)")
    elif "diff" in msg_content and "spoofed" in msg_content:
        await message.reply("Spoofed emails are sending with the brand email domains (noreply@stockx.com) and normal email is sent from our domain (noreply@maisonreceipts.cc)")
    elif "need" in msg_content and "pay" in msg_content:
        await message.reply("Unfortunately, this service is not free. You can check out the prices here -> <#1335030021655494766>")
    elif "it" in msg_content and "paid" in msg_content:
        await message.reply("Unfortunately, this service is not free. You can check out the prices here -> <#1335030021655494766>")
    elif "receive" in msg_content and "email" in msg_content:
        await message.reply("If you didn't receive your email, check your spam folder and remove the mail from the spam folder to get the images to load. If you didn't receive the email in the spam, make sure you entered the correct email address.")
    elif "/gen" in msg_content:
        await message.reply("Check out <#1335030021655494766> to see how you can generate!")


    if message.channel.id != int(config.get("pic_channel")):
        return
    else:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                await message.reply(f"```{attachment.url}```")
                return
            


    await bot.process_commands(message)


bot.run(config['tokens']['main'])