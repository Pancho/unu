def execute(request):
	return {
		'grid': True if 'grid' in request.GET else False,
	}
