import csv
from unique_id import get_id

class CSV_Archive:

	def __init__(self,file_name,permission,*fields):

		self.file_name = file_name
		self.permission = permission
		self.fields = list(fields)
		self.dict = {'ID':0}

	
		for n,field in enumerate(self.fields):
			field_name = field[0]
			field_permission = field[1]
			self.dict[field_name] = n+1

		try:
			f = open(self.file_name,'r',encoding='utf-8',newline='')
		except:
			f = open(self.file_name,'w',encoding='utf-8',newline='')
			csv_writer = csv.writer(f,delimiter=',',quoting=csv.QUOTE_ALL)
			header = self.fields.copy()
			header.insert(0,('ID','U'))
			csv_writer.writerow([field_name for field_name,field_permission in header])
		f.close()

		

	def write(self, items):

		current_f = self.read()
		for data in current_f:
			data.pop(0)
		
		with open(self.file_name,'a', encoding='UTF-8', newline='') as f:
			csv_writer = csv.writer(f,delimiter=',', quoting=csv.QUOTE_ALL)

			# Test unique row
			lines_write = []
			for item in items:
				for data in current_f:
					if self.permission == 'U':
						item_str = ''.join(item)
						data_str = ''.join(data)
						if item_str == data_str:
							break

					for column, field in enumerate(self.fields):
						if field[1] == 'U':
							if item[column] == data[column]:
								break

					else:
						continue
					break
			
				else:
					current_f.append(item)
					lines_write.append(item)


			# Write the remaining row to the file
			for line in lines_write:
				line.insert(0, get_id())
				csv_writer.writerow(line)
			

	def read(self):

		data = []

		with open(self.file_name,'r', encoding='UTF-8', newline='') as f:
			f_reader = csv.reader(f)

			for line in list(f_reader)[1:]:
				data.append(line)

			return data



	def find(self, field_name, field_value):

		current_f = self.read()
		find_index = self.dict[field_name]
		all_matches = []
		for item in field_value:
			matching_lines = []
			for line in current_f:

				if item[0] == line[find_index]:
					matching_lines.append(line)

			if matching_lines != []:
				all_matches.append(matching_lines)
			else:
				all_matches = []

		return all_matches



	def search(self,results, *argss):

		filters = list(argss)
		current_f = self.read()
		all_matches = []

		for row in current_f:
			
			field_matches = []


			for n,field in enumerate(row):

				for filter_name, operator, filter_value in filters:

					if n == self.dict[filter_name]:

						if operator == '==':


							for value in filter_value:

								if value == field:

									field_matches.append('True')
									break

							else:

								field_matches.append('False')


						if operator == '!=':


							for value in filter_value:

								if value == field:

									field_matches.append('False')
									break

							else:

								field_matches.append('True')


			if 'False' not in field_matches:
				if(results[0] == '*'):
					all_matches.append(row)
				else:
					resulting_row = []
					for n,field in enumerate(row):
						for result in results:
							if n == self.dict[result]:
								resulting_row.append(field)


					all_matches.append(resulting_row)
							
			
		return all_matches