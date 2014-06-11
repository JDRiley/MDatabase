from django.http import HttpResponse
from django.template import RequestContext, loader

from django.shortcuts import render


from Network_Data import create_selection_pack
from MDatabase import controller_tag
def hello(i_request):
	context = {'output_str': 'Hello'}
	return render(i_request, './hello.html', context)

def network_data(i_request):
	context = {'selection_pack' : create_selection_pack(i_request)}
	context['output_str'] = 'Network_Data'
	return render(i_request, './network_data.html', context)


def controller_tag_render_func(i_request):
	
	return render(i_request, './controller_tag.html', controller_tag.get_context(i_request))