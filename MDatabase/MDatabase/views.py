from django.http import HttpResponse
from django.template import RequestContext, loader

from django.shortcuts import render


from Network_Data import create_data_pack

def hello(i_request):
	context = {'output_str': 'Hello'}
	return render(i_request, './hello.html', context)

def network_data(i_request):
	context = {'data_pack' : create_data_pack(i_request)}
	context['output_str'] = 'Network_Data'
	return render(i_request, './network_data.html', context)

