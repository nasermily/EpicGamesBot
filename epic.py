import utils
import datetime

EPIC_URL = "https://www.epicgames.com/store/en-US/free-games"
GREEN = 0x3d9c3d
RED = 0x822c2c


"""
Returns the next Epic Games date from the data.txt file.
:return: Datetime for next Epic Games release
"""
def get_epic_file_data():
  return datetime.date.fromisoformat(utils.grab_file_data(utils.EPIC_GAMES_LINE_NUM).strip('\n'))

"""
Scrapes Epic Games for the free games available. Grabs all link elements on the page and checks to see if they're labelled as 'Free Games' then grabs the relevant data. Probably not the most efficient way to do this. Try/except is there since a majority of the links do not have an attribute for 'aria-label' and an error will be thrown if there isn't one.
:return: A list of embeds for each free game on Epic
"""
def get_games():
  embeds = []
  driver = utils.init_driver()
  next_game_time = get_epic_file_data()

  driver.get(EPIC_URL)
  elements = driver.find_elements_by_tag_name('a')
  for game in elements:
    try:
      if(game.get_attribute("aria-label").startswith("Free Game")):
        color = GREEN
        label = game.find_element_by_xpath('.//*[@data-testid="offer-title-info-title"]').text
        link = game.get_attribute('href')
        thumbnail = game.find_element_by_tag_name('img').get_attribute('src')
        date_and_time = game.find_element_by_xpath('.//*[@data-testid="offer-title-info-subtitle"]')
        date_range = date_and_time.text.split('at')[0]
        if not date_range.startswith("Free Now"):
          print(label)
          color = RED
          date_time = date_and_time.find_element_by_tag_name('time').get_attribute('datetime').split('T')[0] # 2021-09-02T15:00:00.000Z
          d = datetime.date.fromisoformat(date_time)
          if d > next_game_time:
            next_game_time = d
            utils.edit_file_data(date_time, utils.EPIC_GAMES_LINE_NUM)
            
        embeds.append(utils.create_embed(label, link, thumbnail, date_range, color))
    except AttributeError:
      print("No label found for: ", game.get_attribute('href'))
    
  return embeds

