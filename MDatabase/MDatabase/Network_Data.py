
import MySQLdb

class Data_Pack:
	def __init__(self, i_con):
		self.row_header = ['Controller_Name',  'Date', 'IP_Address', 'IF_Index', ' AP_ID', 
				'AP_Name', 'Assoc', 'Thruput', 'Channel_Utility', 'Noise', 'Retry_Percentage', 
				'Mgmt_Percentage', 'Beacon_Percentage', 'Probe_Percentage',	'Neighborhood', 
				'Loss_Percentage', 'Channel']


		self.rows = 17
		self.begin_row = 0
		self.end_row = 0

		
		cursor = i_con.cursor()

		cursor.execute('SELECT DISTINCT Controller_Name FROM Dot11Radio')

		self.controller_names = ['All Controllers']

		for controller_name in cursor.fetchall():
			self.controller_names.append(controller_name[0])

		
		





def create_data_pack(i_request):
	a = 4;
	a = a*a;


	con = MySQLdb.connect('141.213.135.146', 'jomike', 'deldeldel', 'MInternet', 3306)
	return_pack = Data_Pack(con)
	return return_pack