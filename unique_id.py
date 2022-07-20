


try:
	# Check if the file excists
	f = open('unique_id.txt','r')
except:
	# if error create the file and add the first number
	f = open('unique_id.txt','w')
	f.write('0')
	f.close()


def get_id():
	# Add a new number
	f = open('unique_id.txt','r+')
	number = int(f.read())
	number += 1
	f.truncate(0)
	f.seek(0) 
	f.write(str(number))
	f.close()

	return str(number)




