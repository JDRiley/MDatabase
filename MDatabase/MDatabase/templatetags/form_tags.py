from django import template

register = template.Library()


def range_form_input(i_name, i_low_val, i_high_val):
	return {'t_name' : i_name, 't_low_val' : i_low_val, 't_high_val' : i_high_val}

register.inclusion_tag('range_form_input.html')(range_form_input)
