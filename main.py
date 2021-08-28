import os
import discord
import datetime
from discord.ext import tasks
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

Epic_URL = "https://www.epicgames.com/store/en-US/free-games"
Bot_Token = os.environ['botToken']
Client = discord.Client()
Channel = None
Next_Game_Time = None

"""
Grabs stored data in case of any bot downtime. Data is simply stored in a text file currently. Each line represents the following:
0: Channel ID
1: Epic Games next free game date/time
"""
def grab_file_data(channel, next_game_time):
  with open("./data.txt", "r") as file:
    for i, line in enumerate(file):
      if (i == 0) and (channel == None):
        channel = Client.get_channel(line)
      elif (i == 1) and (next_game_time == None):
        next_game_time = datetime.datetime(2021, 1, 1)

"""
Writes data to text file line in case of any downtime. Each line represents the following:
0: Channel ID
1: Epic Games next free game date/time
"""
def edit_file_data(data, line_num):
  with open("./data.txt", "r") as file:
    lines = file.readLines()

  lines[line_num] = data

  with open("./data.txt", "w") as file:
    file.writeLines(lines)


"""
Initializes the selenium webdriver for chrome with headless settings
:return: The webdriver
"""
def init_driver():
  options = Options()
  options.headless = True
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  return webdriver.Chrome(options=options)

"""
Creates an embed message for a Free Epic Game
:param - label: Title of the game
:param - link: Link to the game
:param - thumbnail: Image of the game
:param - date_range: The date range the game is free
:return: Formatted embed
"""
def create_embed(label, link, thumbnail, date_range):
  if date_range.startswith("Free Now"):
    embed_color = 0x3d9c3d
  else:
    embed_color = 0x822c2c
  embed = discord.Embed(title=label, url=link, description=date_range, color=embed_color)
  embed.set_image(url=thumbnail)
  return embed

"""
Scrapes Epic Games for the free games available. Grabs all link elements on the page and checks to see if they're labelled as 'Free Games' then grabs the relevant data. Probably not the most efficient way to do this. Try/except is there since a majority of the links do not have an attribute for 'aria-label' and an error will be thrown if there isn't one.
:return: A list of embeds for each free game on Epic
"""
def get_games():
  embeds = []
  driver = init_driver()
  driver.get(Epic_URL)
  elements = driver.find_elements_by_tag_name('a')
  for game in elements:
    try:
      if(game.get_attribute("aria-label").startswith("Free Game")):
        label = game.find_element_by_xpath('.//*[@data-testid="offer-title-info-title"]').text
        link = game.get_attribute('href')
        thumbnail = game.find_element_by_tag_name('img').get_attribute('src')
        date_and_time = game.find_element_by_xpath('.//*[@data-testid="offer-title-info-subtitle"]').text.split('at')
        date_range = date_and_time[0]
        embeds.append(create_embed(label, link, thumbnail, date_range))
    except Exception:
      print("No label found for: ", game.get_attribute('href'))
    
  return embeds

"""
TODO: Add @task.loop(hours=24) check case + date, add role pings, add twitch prime skin checking too?
"""

"""
Event for when the bot is ready.
"""
@Client.event
async def on_ready():
  print("Ready")
  grab_file_data(Channel, Next_Game_Time)
  daily_check()

"""
Event for when a message is posted in the channel. The following commands are supported:
%setChannel: sets the channel notifications to that channel
%check: manually checks and prints free status
%help: prints a help message to server with command list
"""
@Client.event
async def on_message(message):
  if message.author == Client.user:
    return
  if message.content.startswith('%setChannel') or message.content.startswith('%setchannel'):
    Channel = message.channel
    edit_file_data(message.channel.id, 0)
    await Channel.send("Notifications will now be posted in this channel.")
  elif message.content.startswith('%check') or message.content.startswith('%Check'):
    embeds = get_games()
    for embed in embeds:
      await message.channel.send(embed=embed)
  elif message.content.startswith('%help') or message.content.startswith('%Help'): 
    await message.channel.send("help message")

"""
Looping task to check everyday if new games have been released
"""
@tasks.loop(seconds=10)
async def daily_check():
  print("check")
  await Channel.send("Minutely check message")

Client.run(Bot_Token)

