from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SelfMailViews,send_email, openai_function,newsletter

routers = DefaultRouter()

routers.register('', SelfMailViews, basename="self_mail")


urlpatterns = [
    path('send_email/', send_email, name="send_email"),
    path('openai/', openai_function, name="openai"),
    path('newsletter/', newsletter, name="newsletter"),
] + routers.urls

