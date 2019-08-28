import sqlite3
import pandas

class data(object):
	def __init__(self):
		self.base_query = "SELECT {columns} FROM {table}"
		self.player_id_cols =["mlb_name","mlb_id","rotowire_name","rotowire_id",
							  "retro_name","rotowire_pos","retro_id"]
		self.current_year_condition = {"WHERE":{"gameid":{"like":"'%2018%'"}},
										"OR":{"gameid":{"like":"'%2017%'"}}}
	@staticmethod
	def _add_conditions(condition_dict: dict):
		condition_string = """"""
		for k, v in condition_dict.items():
			condition_string += str(k.upper()) + " "
			condition_string += str(list(v.keys())[0]) + " "
			condition_string += str(list(list(v.values())[0].keys())[0]) + " "
			condition_string += str(list(list(v.values())[0].values())[0]) + "\n"
		return condition_string

	@staticmethod
	def _structure_cols(columns: list):
		column_string = ",".join(columns)
		return column_string

	def make_connection(self, db):
		con = sqlite3.connect(db)
		return con

	def get_data(self, db, table, cols="*" ,condition_dict=None):
		if cols != "*":
			cols = self._structure_cols(cols)
		q = self.base_query.format(columns=cols, table=table)
		
		if condition_dict != None:
			condition_string = self._add_conditions(condition_dict)
			q += " " + condition_string
		con = self.make_connection(db)
		df = pandas.read_sql_query(sql=q, con=con)
		con.close()
		return df
