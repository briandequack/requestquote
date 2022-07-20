import CSV_Archive
import random
import Inbox
import threading


f_quotes = CSV_Archive.CSV_Archive('quotes_text.csv', 'A', ('author_ID', 'A'), ('quote', 'U'))
f_send = CSV_Archive.CSV_Archive('send.csv', 'U', ('email_ID', 'A'),('quote_ID', 'A'))
f_authors = CSV_Archive.CSV_Archive('quotes_author.csv', 'A', ('name', 'U'))
f_emails = CSV_Archive.CSV_Archive('emails_archive.csv', 'A', ('email', 'U'))



def add_email(string):

	address = string.split()[-1]
	if address[0] == '<' and address[-1] == '>':
		string = string.split()[-1][1:-1]	
	else:
		string = string.split()[-1]
	
	f_emails.write([[string]])
	print('Stored email:',string)


def get_email_id(string):

	address = string.split()[-1]
	if address[0] == '<' and address[-1] == '>':
		string = string.split()[-1][1:-1]	
	else:
		string = string.split()[-1]
	return f_emails.search(('ID',),('email','==', [string]))[0]


def get_random_quote(email_ID):

	recieved_quotes = f_send.search(('quote_ID',),('email_ID','==', email_ID))

	available_quotes = f_quotes.search(('*',),('ID', '!=', [item.pop(0) for item in recieved_quotes]))
	
	random_quote = available_quotes.pop(random.randint(0, len(available_quotes)))

	quote_author = f_authors.search(('name',),('ID','==', [random_quote[1]]))

	f_send.write([[email_ID[0],random_quote[0]]])
	
	return quote_author[0][0], random_quote[2], len(recieved_quotes)





def main():

	threading.Timer(60.0, main).start()

	emails = Inbox.fetch()

	print(f'Inbox has({len(emails)})')

	for email in emails:

		add_email(email['From'])

		print(email['From'])

		email_ID = get_email_id(email['From'])

		quote_author, quote_text, n = get_random_quote(email_ID)

		print(quote_author, quote_text, n)

		Inbox.send(email['From'],'Your random quote', f'"{quote_text}"\r\n\r\n-{quote_author}')

	Inbox.delete(emails)

main()
