from django import template

register = template.Library()


def range_form_input(i_name, i_low_val, i_high_val):
	return {'t_name' : i_name, 't_low_val' : i_low_val, 't_high_val' : i_high_val}

register.inclusion_tag('range_form_input.html')(range_form_input)


def selection_table(i_selection_pack, i_action_url):
	return {'t_action_url' : i_action_url, 't_selection_pack' : i_selection_pack}

register.inclusion_tag('selection_table.html')(selection_table)


def datetime_range_input(i_name, i_begin_date, i_end_date):
	return {'t_name' : i_name, 't_low_val' : i_begin_date, 't_high_val' : i_end_date}


register.inclusion_tag('datetime_range_input.html')(datetime_range_input)