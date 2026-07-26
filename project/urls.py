"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.landing,name='landing'),
    path('show_users/',views.show_users,name='show_users'),
    path('shopbycategory/',views.shopbycategory,name='shopbycategory'),
    path('shopbycollection/',views.shopbycollection,name='shopbycollection'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('policy/',views.policy,name='policy'),
    path('search/',views.search,name='search'),
    path('category/<int:id>/', views.category_products, name='category_products'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('landing/account/',views.account,name='account'),
    path('landing/userprofile/<int:pk>',views.userprofile,name='userprofile'),
    path('landing/userprofile/profile_data/<int:pk>',views.profile_data,name='profile_data'),
    path('landing/userprofile/my_orders/<int:pk>',views.my_orders,name='my_orders'),
    path('signup/',views.signup,name='signup'),
    path('signupdata/',views.signupdata,name='signupdata'),
    path("cart/", views.cart_page, name="cart_page"),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('login/',views.login,name='login'),
    path('logindata/',views.logindata,name='logindata'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('new_pass/',views.new_pass,name='new_pass'),
    path('reset/',views.reset,name='reset'),
    path('pay_amount/',views.pay_amount,name='pay_amount'),
    path('pay_status/',views.pay_status,name='pay_status'),
    path('logout/',views.logout,name='logout'),
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('add_category/',views.add_category,name='add_category'),
    path('add_category/save_category/',views.save_category,name='save_category'),
    path('show_category/',views.show_category,name='show_category'),
    path('show_category/edit-category/<int:pk>/', views.edit_category, name='edit_category'),
    path('show_category/update_category/<int:pk>/', views.update_category, name='update_category'),
    path('show_category/delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('add_product/',views.add_product,name='add_product'),
    path('add_product/save_product/',views.save_product,name='save_product'),
    path('show_product/',views.show_product,name='show_product'),
    path('show_product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('show_product/update/<int:pk>/', views.update_product, name='update_product'),
    path('show_product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('add_product_image/',views.add_product_image,name='add_product_image'),
    path('add_product_image/save_product_image/',views.save_product_image,name='save_product_image'),
    path('show_product_image/',views.show_product_image,name='show_product_image'),
    path('add_product_size/',views.add_product_size,name='add_product_size'),
    path('add_product_size/save_product_size',views.save_product_size,name='save_product_size'),
    # path('show_product_size/',views.show_product_size,name='show_product_size'),
    path('landing/search/',views.search,name='search'),
    path('landing/bag/',views.bag,name='bag'),
    path('policy/',views.policy,name='policy'),
    path('fitguide/',views.fitguide,name='fitguide'),
    path('otc/',views.otc,name='otc'),
    path('success/',views.success,name='success'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
