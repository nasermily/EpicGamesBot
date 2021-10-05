import utils
import datetime
from selenium.webdriver.common.keys.Keys import RETURN

LEAGUE_URL = "https://gaming.amazon.com/intro"

"""
Grabs the next League skin date
:return: datetime of next skin release
"""
def get_league_file_data():
  return datetime.date.fromisoformat(utils.grab_file_data(utils.LEAGUE_SKINS_LINE_NUM).strip('\n'))

"""

"""
def get_skins():
  driver = utils.init_driver()
  # next_skin_time = get_league_file_data()

  driver.get(LEAGUE_URL)
  driver.implicitly_wait(10)
  element = driver.find_element_by_xpath('.//*[@data-a-target="offer-section-offer-cards"]')
  offers = element.find_elements_by_tag_name('button')
  for offer in offers:
    if(offer.text.startswith("League of Legends")):
      offer.send_keys(RETURN)

      skins = driver.find_elements_by_xpath('.//*[@data-a-target="CallToAction"]')
      for skin in skins:
        print(skin.text)

      return ""
  
  
  return ""

  