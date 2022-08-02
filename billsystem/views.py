from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
# views.py
from .custom_serializer import CustomTokenObtainPairSerializer, InActiveUser
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import status
from django.http import HttpResponse

index = never_cache(TemplateView.as_view(template_name='index.html'))
def image(request):
    image_data = open("build/logo512.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")

def logo(request):
    image_data = open("build/logo.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")

def logo(request):
    image_data = open("build/logo.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")

def favicon(request):
    image_data = open("build/favicon.ico", "rb").read()
    return HttpResponse(image_data, content_type="image/png")

def defaultuser(request):
    image_data = open("build/defaultuser.webp", "rb").read()
    return HttpResponse(image_data, content_type="image/png")

class CustomTokenObtainPairView(TokenViewBase):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            raise InActiveUser()
        except TokenError:
            raise InvalidToken()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)