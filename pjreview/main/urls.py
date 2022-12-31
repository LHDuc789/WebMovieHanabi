from django.urls import path
from . import views

app_name="main" #use for dynamic routing URLs

urlpatterns = [
    path('',views.home,name="home"),
    path('search/',views.search_product,name="search"),
    path('sortlikeaverage/',views.sort_like_average,name="sort_like_average"),
    path('sortviews/',views.sort_views,name="sort_views"),
    path('allProducts/',views.allProducts,name="allProducts"),
    path('details/<int:id>/',views.detail, name='detail'),
    path('like/<int:id>',views.like_product, name='like_product'),
    path('watch/<int:id>/<int:ep>',views.watch_movie, name='watch'),
    path('addproduct/',views.add_product, name='add_product'),
    path('editproduct/<int:id>/',views.edit_product, name='edit_product'),
    path('deleteproduct/<int:id>/',views.delete_product, name='delete_product'),
    path('addreview/<int:id>/',views.add_review, name='add_review'),
    path('editreview/<int:product_id>/<int:review_id>/',views.edit_review, name="edit_review"),
    path('deletereview/<int:product_id>/<int:review_id>/',views.delete_review, name="delete_review"),
    path('likeuser/<int:id>/',views.liked_user, name="likeuser"),
    path('sortyear/<int:year>/',views.sort_year, name="sortyear"),
    path('listoftypes/',views.list_of_types, name = "list_of_types"),
    path('sorttype/<str:name>/',views.sort_by_type, name="sort_by_type"),
]