from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_pic(request):
    return_message = str()
    if request.method == 'GET':
        try:
            param = request.GET
            path = param.__getitem__('i')

            # Return the picture somehow
            return_message = path

        except Exception as e:
            return HttpResponseBadRequest(str(e))
    else:
        return HttpResponseBadRequest('Not a GET request.')
    return HttpResponse(return_message)
