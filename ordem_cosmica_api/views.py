from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view()
def teste(request):
    return Response({
        'teste': True
    })
