import requests
import bs4 
import re
import CSV_Archive


quotes = []
page_num = 1

while True:

	base_url = 'https://quotes.toscrape.com/page/{}'.format(page_num)
	res = requests.get(base_url)
	soup = bs4.BeautifulSoup(res.text,'lxml')

	print(f'Scraping: {base_url}')

	if soup.select('.quote') == []:

		break

	else:

		for quote in soup.select('.quote'):

			name = quote.select('.author')[0].text
			text = quote.select('.text')[0].text

			quotes.append([name,text])

		page_num += 1


raw_data = CSV_Archive.CSV_Archive('raw_quotes.csv', 'A', ('name', 'A'), ('text', 'U'))
raw_data.write(quotes)



