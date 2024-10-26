from django.urls import path
from .views import EventListView, AddToCartView, PurchaseAllTicketsView, UserTicketsView, UserCartTicketsView, \
    CreateHallView, CreateSectorView, CreateEventView, SetEventSectorPriceView, HallListView, EventSectorListView, \
    EventDeleteView, EventSectorDeleteView, SectorDeleteView, EventListAllView, RemoveFromCartView

urlpatterns = [
    path('events/<int:hall_id>', EventListView.as_view()),
    path('events', EventListAllView.as_view()),
    path('event/<int:event_id>/sectors', EventSectorListView.as_view()),
    path('halls', HallListView.as_view()),
    path('hall/<int:hall_id>', EventListView.as_view()),
    path('cart/add', AddToCartView.as_view()),
    path('cart/purchase', PurchaseAllTicketsView.as_view()),
    path('cart/delete/<int:cart_ticket_id>', RemoveFromCartView.as_view()),
    path('cart', UserCartTicketsView.as_view()),
    path('tickets', UserTicketsView.as_view()),

    path('admin/hall/add', CreateHallView.as_view()),
    path('admin/hall/delete/<int:hall_id>', CreateHallView.as_view()),
    path('admin/sector/add', CreateSectorView.as_view()),
    path('admin/sector/delete/<int:sector_id>', SectorDeleteView.as_view()),
    path('admin/event/add', CreateEventView.as_view()),
    path('admin/event/delete/<int:event_id>', EventDeleteView.as_view()),
    path('admin/event/<int:event_id>/<int:sector_id>', EventSectorDeleteView.as_view()),
    path('admin/event/sector/price', SetEventSectorPriceView.as_view()),
]