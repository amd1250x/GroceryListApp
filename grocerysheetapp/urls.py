from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('glist_viewer/<int:glist_id>', views.GroceryListDetailView, name="glist_view"),

    path('glists', views.glists, name="glists"),
    path('glist/<int:glist_id>', views.glist, name='glist'),

    path('glist/<int:glist_id>/items', views.items, name="items"),
    path('glist/<int:glist_id>/item/<int:item_id>', views.item, name="item"),

    path('glist/<int:glist_id>/persons', views.persons, name="persons"),
    path('glist/<int:glist_id>/person/<int:person_id>', views.person, name="person"),

    path('glist/<int:glist_id>/<int:item_id>/<int:person_id>/add', views.AddPersonToItem, name="addpersontoitem"),
    path('glist/<int:glist_id>/<int:item_id>/<int:person_id>/rem', views.RemPersonFromItem, name="rempersonfromitem"),

    path('glist/<int:glist_id>/calculate', views.CalculateRequest, name="calculate")
    
]