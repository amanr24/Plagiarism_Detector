from django.urls import path
from . import views


app_name = "fileapp"


urlpatterns = [
    path("",views.index,name="home"),
    path("home2",views.index1,name="home2"),
    path("upload",views.send_files,name="uploads"),
]