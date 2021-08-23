import os
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

urlHome = "https://www.epicgames.com/store/en-US/free-games"
botToken = os.environ['botToken']
client = discord.Client()

def createEmbed(label, link, thumbnail, dateRange):
  if dateRange.startswith("Free Now"):
    embedColor = 0x3d9c3d
  else:
    embedColor = 0x822c2c
  embed = discord.Embed(title=label, url=link, description=dateRange, color=embedColor)
  embed.set_image(url=thumbnail)
  return embed

def getGames():
  embeds = []
  options = Options()
  options.headless = True
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=options)
  driver.get(urlHome)
  elements = driver.find_elements_by_class_name("css-53yrcz-CardGridDesktopLandscape__cardWrapperDesktop");
  for game in elements:
    label = game.find_element_by_xpath('.//*[@data-testid="offer-title-info-title"]').text
    link = game.find_element_by_tag_name('a').get_attribute('href')
    thumbnail = game.find_element_by_tag_name('img').get_attribute('src')
    dateAndTime = game.find_element_by_xpath('.//*[@data-testid="offer-title-info-subtitle"]').text.split('at')
    dateRange = dateAndTime[0]
    embeds.append(createEmbed(label, link, thumbnail, dateRange))
    
  return embeds

@client.event
async def on_ready():
  print("Ready")

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('%check') or message.content.startswith('%Check'):
    embeds = getGames()
    for embed in embeds:
      await message.channel.send(embed=embed)
  elif message.content.startswith('%') or message.content.startswith('%help'): 
    await message.channel.send("help message")


client.run(botToken)

