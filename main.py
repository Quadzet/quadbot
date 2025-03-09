import os
import discord
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
import random
from pathlib import Path
import json
import datetime
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = Intents.all()
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='?', intents=intents)

TAG_USAGE = '\n'.join([
   f'Adds or removes a tag from the bot. Usage:',
   f'Add a tag:',
   f'   ?tag + [tag_name] [content]',
   f'Remove a tag:',
   f'   ?tag - [tag_name]',
])

@bot.command(name='tag', help=TAG_USAGE)
@commands.has_role('Admin')
async def add_tag(ctxt):
  message = ctxt.message
  _, _, content = message.content.partition(" ")
  suffix, _, content = content.partition(" ")
  tag, _, content = content.partition(" ")

  if suffix not in {'+', '-'}:
    ctxt.send('\n'.join('Invalid use of the tag command, see the usage help:', TAG_USAGE))
    return

  if suffix == '+':
    for attachment in message.attachments:
      path = Path(attachment.filename)
      await attachment.save(path)

    tag_data = {
      'attachments': [],
      'message': "",
    }
    tag_data['message'] = content
    for attachment in message.attachments:
      path = Path(attachment.filename)
      file = discord.File(path)
      tag_data['attachments'].append(file.filename)

    with open('tags.json', 'r+') as f:
      data = json.load(f)
      data[f'{tag}'] = tag_data
      f.seek(0)
      json.dump(data, f, indent=4)
      f.truncate()

      await ctxt.send(f'Saved tag {tag}.')
      return

  if suffix == '-':
    with open('tags.json', 'r') as f:
      data = json.load(f)

    data.pop(f'{tag}', None)

    with open('tags.json', 'w') as f:
      json.dump(data, f, indent=4)

    await ctxt.send(f'Removed tag {tag}.')
    return

@bot.listen()
async def on_message(message):
  if message.author == bot.user:
      return

  tags = re.findall(r"\?[a-zA-Z0-9]+\b", message.content)
  if tags:
    with open('tags.json', 'r') as f:
      data = json.load(f)
      for tag in tags:

  # tag, _, _ = message.content.partition(" ")
  # prefix = tag[0:1]
  # tag = tag[1:]

  # if prefix != '?':
  #   return
        tag = tag[1:]
        if (tag in {'tag', 'help'}):
          continue

        tag_data = data.get(f'{tag}', None)
        if (tag_data):
          attachments = []
          for attachment in tag_data.get('attachments', None):
            attachments.append(discord.File(attachment))
          await message.channel.send(content=tag_data.get('message', None), files=attachments)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'{datetime.datetime.now()} Unhandled message: {args[0]}\n')
        else:
            raise
  
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)

# todo:
# - monkey spin
# - rein dab
# - knuckle up
# - lakraki slam?
# - twitch clips
# 
# - ?tag +/-
# - ?tag +=
# - file structure for attachments
# - move out globals into env
# - error handling missing files
