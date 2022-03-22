from django.urls import path
from . import views

# # numeron本体
urlpatterns = [
    path("numeron/", views.index, name="numeron"),
    path("reply/", views.reply, name="reply"),
]
