# Dependencies
import time, re, csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from return_stats import return_stats

# Twitter Bot
class TwitterBot:

  # initialize instance
  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.chrome_options = Options()
    self.chrome_options.add_argument("--start-maximized")
    self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
    self.handles =['term1', 'term2', 'term3'] # these should be your search terms. placeholders used here

  # login
  def login(self):
    print("=> Visiting twitter.com")
    try:
      login_url = 'https://twitter.com'
      driver = self.driver
      driver.get(login_url)
      # wait for page to load
      time.sleep(3)
    except Exception as e:
      print(e)
    else:
      print('=> Logging into Twitter')
      time.sleep(3)
      # target username and password fiels and login
      username_field = driver.find_element_by_class_name('email-input')
      password_field = driver.find_element_by_name('session[password]')
      # clear fields, input username and password and submit
      username_field.clear()
      password_field.clear()
      username_field.send_keys(self.username)
      password_field.send_keys(self.password)
      driver.find_element_by_class_name('js-submit').click()
      # wait for home page to load
      time.sleep(5)

  # switch to explore mode to do advanced search
  def switch_to_explore(self):
    print("=> Switching to explore mode")
    driver = self.driver
    try:
      driver.get("https://twitter.com/explore")
      time.sleep(5)
      # locate search field and clear it from search terms
      search_field = driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
      search_field.clear()
      time.sleep(3)
    except Exception as e:
      print(e)

  # loop through search terms and scrape data
  def search_and_collect_data(self):
    print("=> Looping through search terms and collecting data")
    self.my_dict = [] # data container    
    for handle in self.handles:
      driver = self.driver
      search_field = driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
      do_i_wait = True # this is so that the for loop waits for the while loop to finish before moving to the next search term
      # clear field and enter new search term
      search_field.send_keys(Keys.CONTROL + "a")
      search_field.send_keys(Keys.DELETE)
      time.sleep(1)
      search_field.send_keys(handle)
      search_field.send_keys(Keys.RETURN)
      time.sleep(5)

      while do_i_wait:
        articles = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
        if articles == []: # if search returns zero items move to the next search term
            do_i_wait = False
        else:
          while True: # handling endless scrolling / dynamically loaded data
            combined = driver.execute_script("return window.innerHeight + window.scrollY")
            doc_body_height = driver.execute_script("return document.body.scrollHeight")
            if combined == doc_body_height: # if we reach the bottom of the page continue with next term / break loop
              do_i_wait = False
              break
            else:
              time.sleep(7)
              articles = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
              for article in articles:
                stats = article.find_element_by_xpath('.//div[@role="group"]').get_attribute('outerHTML').split('>')[0]
                self.my_dict.append([article.text, stats])  
              driver.execute_script("window.scrollBy(0, 1000)") # scroll depth can be set here
              time.sleep(7)

  # remove ads and duplicates
  def remove_ads_and_duplicates(self): # twitter loads content dynamically so when gradually srcolling down the page the same tweet(s) are scraped more than once. This function removes duplicates. Ads also sneek into twitter feed.
    print("=> Removing ads and duplicates")
    self.no_ads = [item[0]+ 'collected data' +item[1] for item in self.my_dict if 'Promoted' not in item[0]]
    self.no_duplicates = list(set(self.no_ads))

  # write to csv
  def write_to_csv(self):
    print("=> Writing to csv")
    with open("tweeties.csv", "w") as csv_file:
      csv_writer = csv.writer(csv_file, lineterminator = '\n')
      csv_writer.writerow(['Name', 'Twitter Handle', 'Date', 'Tweet', 'Replies', 'Retweets', 'Likes'])
      pattern = re.compile(r"[^\x00-\x7F]+") # used further down to remove unicode characters so that writing to csv doesn't break
      replies_pattern = re.compile(r"(\d+)\s+replies") # used to extract replies to tweets
      retweets_pattern = re.compile(r"(\d+)\s+Retweets") # used to extract retweets
      likes_pattern = re.compile(r"(\d+)\s+likes") # used to extract likes
      for item in self.no_duplicates:
        # Tweet information (name, handle, date, tweet text)
        item = item.split('collected data')
        Tweet_info = item[0]
        Name = Tweet_info.split('\n')[0]
        Twitter_Handle = Tweet_info.split('\n')[1]
        Date = Tweet_info.split('\n')[3]
        Tweet_Text = re.sub(pattern, '', (''.join(Tweet_info.split('\n')[4:])))
        # Tweet Stats (replies, retweets, likes)
        Tweet_stats = item[1]
        Replies = return_stats(Tweet_stats, replies_pattern)
        Retweets = return_stats(Tweet_stats, retweets_pattern)
        Likes = return_stats(Tweet_stats, likes_pattern)
        csv_writer.writerow([Name, Twitter_Handle, Date, Tweet_Text, Replies, Retweets, Likes])

  # close driver
  def close_driver(self):
    print("=> Closing driver")
    self.driver.close()

# run sequence
wpu_bot = TwitterBot('username', 'password')
wpu_bot.login()
wpu_bot.switch_to_explore()
wpu_bot.search_and_collect_data()
wpu_bot.remove_ads_and_duplicates()
wpu_bot.write_to_csv()
wpu_bot.close_driver()
