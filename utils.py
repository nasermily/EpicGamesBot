from discord import Embed
from discord import utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import linecache

CHANNEL_ID_LINE_NUM = 1
EPIC_GAMES_LINE_NUM = 2
LEAGUE_SKINS_LINE_NUM = 3

EPIC_GAMES_ROLE = "EpicGames"
LEAGUE_ROLE = "LeagueSkins"
ROLES = [EPIC_GAMES_ROLE, LEAGUE_ROLE]
ROLE_ERROR_MESSAGE = "There was an error adding/removing you from the specified role. Make sure to use one of the following:\n" + EPIC_GAMES_ROLE + "\n" + LEAGUE_ROLE
HELP_MESSAGE = "help message"

"""
Grabs stored data in case of any bot downtime. Data is simply stored in a text file currently. Each line represents the following:
1: Channel ID
2: Epic Games next free game date/time
3: League Skins next free date/time

:return: Data at the specific line num
"""
def grab_file_data(line_num):
  return linecache.getline('./data.txt', line_num)

"""
Writes data to text file line in case of any downtime. Each line represents the following:
1: Channel ID
2: Epic Games next free game date/time
3: League Skins next free date/time
"""
def edit_file_data(data, line_num):
  with open("./data.txt", 'r') as file:
    lines = file.readlines()
  
  lines[line_num - 1] = data

  with open("./data.txt", 'w') as file:
    file.writelines(lines)

"""
Creates an embed message for a Free Epic Game
:param - label: Title of the game
:param - link: Link to the game
:param - thumbnail: Image of the game
:param - date_range: The date range the game is free
:return: Formatted embed
"""
def create_embed(label, link, thumbnail, date_range, color):
  embed = Embed(title=label, url=link, description=date_range, color=color)
  embed.set_image(url=thumbnail)
  return embed

"""
Initializes the selenium webdriver for chrome with headless settings
:return: The webdriver
"""
def init_driver():
  options = Options()
  options.headless = False
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  return webdriver.Chrome(options=options)

"""
Adds a user to a specified role
:param - user: User that asked to be added
:param - role: Role to be applied to user
:param - channel: Channel that the verification message can be sent to
"""
async def add_role(user, role, channel):
  try:
    await user.add_roles(utils.get(user.guild.roles, name=role))
  except Exception as e:
    print("There was an error adding a user to " + role + ": " + str(e))
  else:
    await channel.send("You have been added to " + role)

"""
Removes a user from notification roles
:param - user: User that asked to be removed
:param - role: Role to be removed to user
:param - channel: Channel that the verification message can be sent to
"""
async def remove_role(user, role, channel):
  try:
    await user.remove_roles(utils.get(user.guild.roles, name=role))
  except Exception as e:
    print("There was an error removing a user from " + role + ": " + str(e))
  else:
    await channel.send("You have been removed from " + role)

