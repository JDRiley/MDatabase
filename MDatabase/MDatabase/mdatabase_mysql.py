import MySQLdb

def get_mdatabase_connection():
	return MySQLdb.connect('141.213.135.146', 'jomike', 'deldeldel', 'MInternet', 3306)
