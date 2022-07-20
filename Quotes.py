import CSV_Archive


def import_raw_data(file):

	f_quotes_text = CSV_Archive.CSV_Archive('quotes_text.csv', 'A', ('author_ID', 'A'), ('quote', 'U'))
	f_quotes_author = CSV_Archive.CSV_Archive('quotes_author.csv', 'A', ('name', 'U'))
	
	raw_data = CSV_Archive.CSV_Archive(f'{file}.csv', 'A', ('name', 'A'), ('text', 'U'))

	# Extract all authors and text from file
	authors = [author.pop(0) for author in raw_data.search(('name',))]
	texts = [text.pop(0) for text in raw_data.search(('text',))]

	
	#Clean data
	texts_clean = [text[1:-1] for text in texts]
	


	# Write all the author to CSV file
	f_quotes_author.write(raw_data.search(('name',)))

	# Get all the author ids from the CSV file
	author_ids = []
	for author in authors:
		author_id = f_quotes_author.search(('ID',),('name','==', [author]))
		author_ids.append(author_id.pop(0).pop(0))

	# Create new row of author id and the text
	quotes = [list(quote) for quote in zip(author_ids,texts_clean)]

	# Write all the quote text to the CSV file
	f_quotes_text.write(quotes)



import_raw_data('raw_data')
