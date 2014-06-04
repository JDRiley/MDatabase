
import MySQLdb
from django.http import QueryDict

from network_data_helpers import *

ALL_CONTROLLERS_STRING = 'All Controllers'
CONTROLLER_NAME_COLLUMN = 'Controller_Name'
AP_NAME_COLLUMN = 'AP_Name'
ALL_AP_STRING = 'All Aps'
ALL_BUILDINGS_STRING = 'All Buildings'
FILTER_BY_CONTROLLER_STRING = 'Filter By Controller'
def make_in_condition(i_names, i_column_name, i_all_name):
	if(0 == len(i_names)):
		return '1'

	condition = '( '
	for name in i_names:
		if(i_all_name == name):
			return '1'
		elif(condition != '( '):
			condition += ', '
		condition += ('\'' + name + '\'')

	return i_column_name + ' IN' + condition + ')'

class Data_Pack:
	#entry_begin
	#num_entries
	#loss_low
	#loss_high
	#retry_low
	#retry_high
	#thru_low
	#thru_high
	#beacon_low
	#beacon_high
	#probe_low
	#probe_high

	def make_controller_condition(self):
		return make_in_condition(self.selected_controllers
						   , CONTROLLER_NAME_COLLUMN, ALL_CONTROLLERS_STRING)

	def make_ap_name_condition(self):
		return make_in_condition(self.selected_aps
						   , AP_NAME_COLLUMN, ALL_AP_STRING);

	def __init__(self, i_con):
		self.row_header = ['Controller_Name',  'Date' , 'IP_Address', 'IF-Index', ' AP_ID', 
				'AP_Name', 'Assoc', 'Thru', 'Ch-Util', 'Noise', 'Retry%', 
				'Mgmt%', 'Beacon%', 'Probe%',	'Neighbor-hood', 
				'Loss%', 'Channel']

		self.filter_by_controller_str = FILTER_BY_CONTROLLER_STRING
		

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
		self.thru_low = '0'
		self.thru_high = '100'
		

		


		

		return

	def initialize_data(self,i_post_args):
		cursor = self.con.cursor()
		
		self.selected_controllers = i_post_args.getlist('controller_names')
		self.selected_buildings = i_post_args.getlist('buildings')
		self.selected_aps = i_post_args.getlist('access_points')

		submit_flag = i_post_args.has_key('submit')
		print("Submit Flag", submit_flag, FILTER_BY_CONTROLLER_STRING, i_post_args['submit'])

		if( submit_flag and FILTER_BY_CONTROLLER_STRING == i_post_args['submit']):
			self.controller_names = ['All Controllers']
			cursor.execute('SELECT DISTINCT Controller_Name FROM Network_Connections')
			for controller_name in cursor.fetchall():
				self.controller_names.append(controller_name[0])

			in_condition = make_in_condition(self.selected_controllers, CONTROLLER_NAME_COLLUMN
						  , ALL_CONTROLLERS_STRING)

			cursor.execute('SELECT DISTINCT Building_Name FROM Network_Connections WHERE '
				  + in_condition)

			
			self.buildings = []
			for building in cursor.fetchall():
				self.buildings.append(building[0])

			cursor.execute('SELECT DISTINCT AP_Name FROM Network_Connections WHERE '
				  + in_condition)

			self.access_points = [ALL_AP_STRING]
			for access_point in cursor.fetchall():
				self.access_points.append(access_point[0])

		else:
			self.controller_names = ['All Controllers']
			cursor.execute('SELECT DISTINCT Controller_Name FROM Network_Connections')
			for controller_name in cursor.fetchall():
				self.controller_names.append(controller_name[0])
		
			cursor.execute('SELECT DISTINCT Building FROM Buildings')

			self.buildings = [ALL_BUILDINGS_STRING]
			for building in cursor.fetchall():
				self.buildings.append(building[0])

			cursor.execute('SELECT DISTINCT AP_Name FROM Access_Points')

			self.access_points = [ALL_AP_STRING]
			for access_point in cursor.fetchall():
				self.access_points.append(access_point[0])



		self.entry_begin = i_post_args.get('entry_begin')
		self.num_entries = i_post_args.get('num_entries')
		self.loss_low = i_post_args.get('loss_low')
		self.loss_high = i_post_args.get('loss_high')
		self.retry_low = i_post_args.get('retry_low')
		self.retry_high = i_post_args.get('retry_high')
		self.thru_low = i_post_args.get('thru_low')
		self.thru_high = i_post_args.get('thru_high')
		self.beacon_low = i_post_args.get('beacon_low')
		self.beacon_high = i_post_args.get('beacon_high')
		self.probe_low = i_post_args.get('probe_low')
		self.probe_high = i_post_args.get('probe_high')

		conditions = []

		conditions.append(self.make_controller_condition())
		conditions.append(self.make_ap_name_condition())

		loss_condition = '((Loss_Percentage >= ' + self.loss_low\
			+ ') AND (' + ' Loss_Percentage  <= ' + self.loss_high + '))'

		conditions.append(make_condition('Loss_Percentage', self.loss_low, self.loss_high))

		conditions.append(make_condition('Retry_Percentage', self.retry_low, self.retry_high))
		conditions.append(make_condition('Thruput', self.thru_low, self.thru_high))
		conditions.append(make_condition('Beacon_Percentage', self.beacon_low, self.beacon_high))
		conditions.append(make_condition('Probe_Percentage', self.probe_low, self.probe_high))



		query = 'SELECT * FROM Dot11Radio WHERE 1' 

		for f_condition in conditions:
			query +=' AND '
			query += f_condition


		query += ' LIMIT 0, 100'

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
		default_post.update({'controller_names' : ALL_CONTROLLERS_STRING})
		default_post.update({'access_points' : ALL_AP_STRING})
		default_post.update({'buildings' : ALL_BUILDINGS_STRING})
		default_post.update({'entry_begin' : '0'})
		default_post.update({'num_entries' : '10000'})
		
		default_post.update({'loss_low' : '0' })
		default_post.update({'loss_high' : '100' })
		default_post.update({'retry_low' : '0' })
		default_post.update({'retry_high' : '100' })
		default_post.update({'thru_low' : '0' })
		default_post.update({'thru_high' : '100' })
		default_post.update({'beacon_low' : '0' })
		default_post.update({'beacon_high' : '100' })
		default_post.update({'probe_low' : '0' })
		default_post.update({'probe_high' : '100' })
		return_pack.initialize_data(default_post)
		 
	return return_pack


