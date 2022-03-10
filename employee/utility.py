CPSL = 'CPSL'
slant = '/'



def check_code_length(data):
	'''
	Boolean - > True or False

	'''
	if data and len(data) >= 5:
		return True
	return False



def code_format(raw_data):

	'''
	0: only works for 5 alphanumeric length
	1: check existence of data
	2: check length of data
	3: clean data
	4: manipulate data
	5: insert RGL
	6: check length
	7: insert slashes in list
	8: get string representation of code
	9: check if it already exits -> handle that in the view
	10: return code

	eg. A0091 -> RGLA0091 -> RGL/A0/091 
	'''
	if check_code_length(raw_data):
		if not raw_data.startswith('CPSL'):
			grab_list = list(raw_data.strip().upper())
			join_data_cpsl = list(CPSL) + grab_list
			data_list_1 = join_data_cpsl[0:4] + list(slant)
			data_list_2 = join_data_cpsl[4:6] + list(slant)
			data_list_3 = join_data_cpsl[6:]
			data_str = ''.join(data_list_1 + data_list_2 + data_list_3)

			return data_str

		else:
			#assuming raw_data = CPSL/**/***
			return raw_data

	else:
		return
