import os

bot_tok = os.environ['TOKEN']

import random
import asyncio
import json
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.utils import get

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()
default_prefixes = ["get ", "Get", "go ", "Go ", "hit "]

bot = commands.Bot(command_prefix = default_prefixes , description = 'Money.Co', case_insensitive = False)

@cooldown(1, 5, BucketType.default )

#on ready event
@bot.event
async def on_ready():
    await bot.change_presence (status = discord.Status.online,
                               activity = discord.Activity (type = discord.ActivityType.listening,
                               name = "[get ]", 
                               emoji = None))
    print ("Bot is ready \n =======================")
@bot.event
async def on_command_error(ctx, error):
    sid = bot.get_user(569397766996885525)

    if isinstance(error, commands.errors.MissingRequiredArgument):
                await ctx.send(f"You did not provide required arguments for this command")

    elif isinstance(error, commands.errors.CommandNotFound):
        print(ctx, error)

    else:
        await sid.send(f" There was an error, check console for details")
        raise error
        return ""
#loading cogs in main
    # noinspection PyUnboundLocalVariable
cogs_list = os.listdir('./cogs')
for file_name in cogs_list:
    if file_name.endswith(".py"):
        bot.load_extension(f"cogs.{file_name[:-3]}")
        print(f"{file_name} has been loaded")

keep_alive()
# run bot
bot.run(bot_tok)