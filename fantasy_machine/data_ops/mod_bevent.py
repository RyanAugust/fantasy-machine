def correct_bool_cols(event):
	for bool_column in ['abflag','sfflag','shflag']:
		event[bool_column] = event[bool_column].replace('T',True).replace('F',False)
	return event