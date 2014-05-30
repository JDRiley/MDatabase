
import MySQLdb
from django.http import QueryDict

def make_controller_condition(i_controller_names):
		if(0 == len(i_controller_names)):
			return '1'

		condition = '( '
		for name in i_controller_names:
			if('All Controllers' == name):
				return '1'
			elif(condition != '( '):
				condition += ', '
			condition += ('\'' + name + '\'')

		return 'Controller_Name IN' + condition + ')'

class Data_Pack:
	def __init__(self, i_con):
		self.row_header = ['Controller_Name',  'Date' , 'IP_Address', 'IF-Index', ' AP_ID', 
				'AP_Name', 'Assoc', 'Thru', 'Ch-Util', 'Noise', 'Retry%', 
				'Mgmt%', 'Beacon%', 'Probe%',	'Neighbor-hood', 
				'Loss%', 'Channel']


		self.rows = 17
		self.begin_row = 0
		self.end_row = 0

		self.data_rows = []
		self.con = i_con
		self.loss_low = '0'
		self.loss_high = '100'
		self.num_entries = '500'
		self.entry_begin = '0'
		self.retry_low = '0'
		self.retry_high = '100'
		cursor = i_con.cursor()

		cursor.execute('SELECT DISTINCT Controller_Name FROM Dot11Radio')

		self.controller_names = ['All Controllers']

		for controller_name in cursor.fetchall():
			self.controller_names.append(controller_name[0])

		return
		


	
		
	

	def initialize_data(self,i_post_args):
		cursor = self.con.cursor()

		names_list = []


		for f_args in  i_post_args.lists():
			if('controller_names' == f_args[0]):
				names_list = f_args[1]
			elif('loss_low' == f_args[0]):
				self.loss_low = f_args[1][0]
			elif('loss_high' == f_args[0]):
				self.loss_high = f_args[1][0]
			elif('entry_begin' == f_args[0]):
				self.entry_begin = f_args[1][0]
			elif('num_entries' == f_args[0]):
				self.num_entries = f_args[1][0]
			elif('retry_low' == f_args[0]):
				self.retry_low = f_args[1][0]
			elif('retry_high' == f_args[0]):
				self.retry_high = f_args[1][0]



		
		controller_condition = make_controller_condition(names_list)

		loss_condition = '((Loss_Percentage >= ' + self.loss_low\
			+ ') AND (' + ' Loss_Percentage  <= ' + self.loss_high + '))'

		query = 'SELECT * FROM Dot11Radio WHERE ' \
			+ controller_condition + ' AND ' + loss_condition + ' LIMIT 0, 100'
		cursor.execute(query)

		for row in cursor.fetchall():
			self.data_rows.append(row)

		return



def create_data_pack(i_request):
	a = 4;
	a = a*a;


	con = MySQLdb.connect('141.213.135.146', 'jomike', 'deldeldel', 'MInternet', 3306)

	

	return_pack = Data_Pack(con)

	if('POST' == i_request.method):
		return_pack.initialize_data(i_request.POST)
	else:
		default_post = QueryDict('')
		default_post = default_post.copy()
		default_post.update({'controller_names' : 'All Controllers'})
		default_post.update({'loss_low' : '0'})
		default_post.update({'loss_high' : '100'})
		default_post.update({'retry_low' : '0'})
		default_post.update({'retry_high' : '100'})
		default_post.update({'entry_begin' : '0'})
		default_post.update({'num_entries' : '10000'})

		return_pack.initialize_data(default_post)
		 
	return return_pack


