from selenium import webdriver  #importing selenium to use website in the background
from selenium.webdriver.chrome.options import Options  #allows headless setting to be used for Chrome
import time
import csv

url = 'https://stockanalysis.com/stocks/'
DRIVER_PATH = '/Users/joegrey/Code/chromedriver'

#changes settings so when is will be headless browser when opened up later
options = Options()
options.headless = True

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH) #opens headless browser
driver.get(url)

tick_loc = 1
stock_ticker_list = list()
start_letter = 'na'
while True:
    try:
        stock_ticker = driver.find_element_by_xpath(f'/html/body/div[2]/div/div[2]/main/article/div/div/ul/li[{tick_loc}]/a').get_attribute('innerHTML').split()[0]
        if not stock_ticker.startswith(start_letter):
            print('Gathering: ', stock_ticker[0])
            start_letter = stock_ticker[0]
        stock_ticker_list.append(stock_ticker)
        tick_loc += 1
    except Exception as e:
        print(e)
        break
driver.quit()

start_letter = 'na'
with open('stock_ticker_list.csv', mode='w') as ticker_file:
    ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for ticker in stock_ticker_list:
        if not ticker.startswith(start_letter):
            print('Saving: ', ticker[0])
            start_letter = ticker[0]
        ticker_writer.writerow([ticker])

    
