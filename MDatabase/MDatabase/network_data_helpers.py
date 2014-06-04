

def make_condition(i_val_name, i_low_val, i_high_val):
	return '((' + i_val_name + ' >= ' + i_low_val\
		+') AND ( ' + i_val_name + ' <= ' + i_high_val + '))'