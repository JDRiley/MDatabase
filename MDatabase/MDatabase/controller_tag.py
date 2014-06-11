from Network_Data import create_selection_pack
from mdatabase_mysql import get_mdatabase_connection

import time
class Controller_Tag_Form_Values:
	def __init__(self):
		self.add_tags = 'Add Tags'

class Controller_Tag_Form_Names:
	def __init__(self):
		self.add_tags = 'add_tags'

def add_tag_to_database(i_cursor, i_collumn_name, i_item_name, i_tag, i_flag = 'administrative_flag'):
	if(not len(i_tag)):
		return

	query = 'INSERT INTO ' + i_collumn_name + ' VALUES ("' + i_item_name \
		+ '" , "' + i_tag + '" , "' + i_flag + '" , "' + time.strftime('%Y-%m-%d %H:%M:%S') +'" )'

	i_cursor.execute(query)
	
	print(query)


def get_context(i_request):
	selection_pack = create_selection_pack(i_request, 1)
	context = {'selection_pack' : selection_pack}
	context['form_names'] = Controller_Tag_Form_Names()
	context ['form_values'] = Controller_Tag_Form_Values()
	context['output_str'] = 'Controller Tag'
	

	form_names = context['form_names']
	if('POST' != i_request.method):
		return context

	print('Posted')
	post_vals = i_request.POST

	if(not post_vals.has_key(form_names.add_tags)):
		return context

	print('Post Val: ', post_vals[form_names.add_tags])


	con = get_mdatabase_connection()
	cursor = con.cursor()

	for controller_name in selection_pack.selected_controllers:
		
		add_tag_to_database(cursor, 'Controllers', controller_name, post_vals['tag_1'])
		add_tag_to_database(cursor, 'Controllers', controller_name, post_vals['tag_2'])
		add_tag_to_database(cursor, 'Controllers', controller_name, post_vals['tag_3'])
		add_tag_to_database(cursor, 'Controllers', controller_name, post_vals['tag_4'])

	for building_name in selection_pack.selected_buildings:
		
		add_tag_to_database(cursor, 'Buildings', building_name, post_vals['tag_1'])
		add_tag_to_database(cursor, 'Buildings', building_name, post_vals['tag_2'])
		add_tag_to_database(cursor, 'Buildings', building_name, post_vals['tag_3'])
		add_tag_to_database(cursor, 'Buildings', building_name, post_vals['tag_4'])

	for access_point in selection_pack.selected_aps:
		
		add_tag_to_database(cursor, 'Access_Points', access_point, post_vals['tag_1'])
		add_tag_to_database(cursor, 'Access_Points', access_point, post_vals['tag_2'])
		add_tag_to_database(cursor, 'Access_Points', access_point, post_vals['tag_3'])
		add_tag_to_database(cursor, 'Access_Points', access_point, post_vals['tag_4'])

	con.commit()		
		
	return context
