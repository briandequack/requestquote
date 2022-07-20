import imaplib
import email
import smtplib
import getpass


def fetch():

	emails = []
	login = ''
	password = ''

	M = imaplib.IMAP4_SSL('imap.gmail.com')
	M.login(login,password)
	M.list()
	M.select('inbox')
	typ, data = M.search(None,"SUBJECT 'Quote'")

	for email_id in data[0].split():

		result, email_data = M.fetch(email_id, '(RFC822)')
		raw_email = email_data[0][1]

		rew_email_string = raw_email.decode('utf-8')
		email_message = email.message_from_string(rew_email_string)

		sender = email_message['From']
		recipient = email_message['To']
		subject = email_message['Subject']

		for part in email_message.walk():
			if part.get_content_type() == 'text/plain':
				body = part.get_payload(decode=True)

				emails.append({'Subject':subject,'Body':body,'From':sender,'To':recipient, 'ID':email_id})

	M.close()
	M.logout()
	return emails





def delete(stuff):

	login = 'kcauqednairb@gmail.com'
	password = 'bzfihxnsromrgkfi'

	M = imaplib.IMAP4_SSL('imap.gmail.com')
	M.login(login,password)
	M.list()
	M.select('inbox')

	for x in stuff:
		M.store(x['ID'], '+X-GM-LABELS', '\\Trash')

	M.expunge()
	M.close()
	M.logout()



def send(to_address='empty',subject='empty',message='empty'):
	
	smtp_object = smtplib.SMTP('smtp.gmail.com',587)
	smtp_object.ehlo()
	smtp_object.starttls()

	email = 'kcauqednairb@gmail.com'
	password = 'bzfihxnsromrgkfi'
	smtp_object.login(email,password)

	from_adress = email
	msg = "Subject: "+subject+"\n"+message

	print(smtp_object.sendmail(from_adress,to_address,msg))

	smtp_object.quit()


