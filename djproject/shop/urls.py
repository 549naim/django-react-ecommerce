from rest_framework import routers
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

route=routers.DefaultRouter()
route.register("category",views.CategoryView ,basename="categoryview")
route.register("cart",views.Mycart ,basename="cart")
route.register("oldorder",views.Oldorders ,basename="oldorder")


urlpatterns = [
    path("",include(route.urls)),
    path('product/',views.ProductView.as_view(),name='Product'),
    path('product/<int:id>/',views.ProductView.as_view()),
    path('profile/',views.Profileview.as_view(),name='profile'),
    path('userdataupdate/',views.UserdataUpdate.as_view(),name='userdataupdate'),
    path('profileimageupdate/',views.Profileimageupdate.as_view(),name='profileimageupdate'),
    path('addtocart/',views.AddtoCart.as_view(),name='addtocart'),
    path('editcart/',views.Editcart.as_view(),name='editcart'),
    path('deletecart/',views.Deletecart.as_view(),name='deletecart'),
    path('deletefullcart/',views.Deletefullcart.as_view(),name='deletefullcart'),
    path("register/", views.RegisterApiView.as_view(),name='register')

]
