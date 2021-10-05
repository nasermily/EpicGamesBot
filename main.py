import os
import discord
from discord.ext import tasks
import datetime
import utils
import epic
import league

BOT_TOKEN = os.environ['botToken']
Client = discord.Client()

"""
Grabs the channel to print anything to
:return: Channel object
"""
def get_message_channel():
  return Client.get_channel(int(utils.grab_file_data(utils.CHANNEL_ID_LINE_NUM).strip('\n')))

"""
Event for when the bot is ready. Reads in any saved file data in the case of any downtime.
"""
@Client.event
async def on_ready():
  print("Ready")
  daily_check.start()

"""
Event for when a message is posted in the channel. The following commands are supported:
%setchannel: sets the channel notifications to that channel
%check: manually checks and prints free status
%notify [@role]: Adds user to the specified role
%unnotify [@role]: Removes user from specified role
%help: prints a help message to server with command list
"""
@Client.event
async def on_message(message):
  if message.author == Client.user: #Ignore bot's own messages
    return
  elif message.content.lower().startswith('%setchannel'):
    utils.edit_file_data(str(message.channel.id), utils.CHANNEL_ID_LINE_NUM)
    await get_message_channel().send("Notifications will now be posted in this channel.")
  elif message.channel == get_message_channel(): #Only parse messages from desired channel
    if message.content.lower().startswith('%check'):
      embeds = epic.get_games()
      await message.channel.send("@" + utils.EPIC_GAMES_ROLE)
      for embed in embeds:
        await message.channel.send(embed=embed)
    elif message.content.lower().startswith('%notify'):
      role_name = message.content.split("@")[1]
      if(role_name in utils.ROLES):
        utils.add_role(message.author, role_name, message.channel)
      else:
        await message.channel.send(utils.ROLE_ERROR_MESSAGE)
    elif message.content.lower().startswith('%unnotify'):
      role_name = message.content.split("@")[1]
      if(role_name in utils.ROLES):
        utils.remove_role(message.author, role_name, message.channel)
      else:
        await message.channel.send(utils.ROLE_ERROR_MESSAGE)
    elif message.content.lower().startswith('%help'): 
      await message.channel.send(utils.HELP_MESSAGE)

"""
Looping task to check everyday if new games have been released
"""
@tasks.loop(minutes=1)
async def daily_check():
  """
  if datetime.datetime.now().date() >= epic.grab_epic_file_data():
    embeds = epic.get_games()
    await get_message_channel().send("@" + utils.EPIC_GAMES_ROLE)
    for embed in embeds:
      await get_message_channel().send(embed=embed)
  """
  league.get_skins()
    
def main():
    Client.run(BOT_TOKEN)

if __name__ == "__main__":
    main()

