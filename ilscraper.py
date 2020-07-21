from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
import re

column_names = ["Facility", "County", "Total Cases", "Total Deaths"]
df = pd.DataFrame(columns = column_names)

url = 'https://www.dph.illinois.gov/covid19/long-term-care-facility-outbreaks-covid-19'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'), options=options)
driver.get(url)
time.sleep(3)
page = driver.page_source
driver.quit()

html_soup = BeautifulSoup(page, 'html.parser')
#print(html_soup)

main_div = html_soup.find('div', {'id': 'LTCContainer'})

facility_count = 0

for tag in main_div.children:
	if tag.has_attr('class'):
		if tag['class'][0] == 'ui-accordion-header':
			current_county = tag.text.strip()
		else:
			facilities = tag.find_all('div', {'class': 'accordion-content'})
			for facility in facilities:
				name = facility.find('h3').text.strip()
				
				data = facility.find_all('p')
				cases = re.findall('\d+', str(data[0]))
				deaths = re.findall('\d+', str(data[1]))
				
				df = df.append({'Facility' : name , 'County' : current_county, 'Total Cases' : int(cases[0]), 'Total Deaths' : int(deaths[0])} , ignore_index=True)
				facility_count = facility_count + 1

df.to_csv('il_data.csv')
print("There are " + str(facility_count) + " total facilities with cases")
