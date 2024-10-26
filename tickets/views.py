from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Hall, Sector, EventSectorPrice, CartTicket, Ticket
from .serializers import EventSerializer, CartTicketSerializer, HallSerializer, SectorSerializer, \
    EventSectorPriceSerializer, TicketSerializer
from users.views import AuthenticatedAPIView, AdminAuthenticatedAPIView


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = []


class AddToCartView(AuthenticatedAPIView):
    def post(self, request):
        user = self.get_user_from_token(request)
        event_id = request.data['event']
        sector_id = request.data['sector']

        event = Event.objects.get(id=event_id)
        sector = Sector.objects.get(id=sector_id)

        cart_ticket = CartTicket.objects.create(
            event=event,
            sector=sector,
            user=user,
            price=request.data['price'],
            owner_first_name=request.data['owner_first_name'],
            owner_last_name=request.data['owner_last_name']
        )

        serializer = CartTicketSerializer(cart_ticket)
        return Response(serializer.data)

class RemoveFromCartView(AuthenticatedAPIView):
    def delete(self, request, cart_ticket_id):
        try:
            cart_ticket = CartTicket.objects.get(id=cart_ticket_id)
            if cart_ticket.user == self.get_user_from_token(request):
                cart_ticket.delete()
                return Response({'message': 'Ticket successfully removed from cart.'})
            else:
                return Response({'error': 'Something went wrong'})
        except CartTicket.DoesNotExist:
            return Response({'error': 'Ticket in cart not found.'})

class PurchaseAllTicketsView(AuthenticatedAPIView):
    def post(self, request):
        user = self.get_user_from_token(request)

        cart_tickets = CartTicket.objects.filter(user=user)

        if not cart_tickets.exists():
            return Response({'error': 'No tickets in cart'})

        purchased_tickets = []
        for cart_ticket in cart_tickets:
            ticket_data = {
                'owner_first_name': cart_ticket.owner_first_name,
                'owner_last_name': cart_ticket.owner_last_name,
                'event': cart_ticket.event.id,
                'sector': cart_ticket.sector.id,
                'user': user.id,
                'price': cart_ticket.price
            }

            ticket_serializer = TicketSerializer(data=ticket_data)
            if ticket_serializer.is_valid():
                ticket_serializer.save()
                purchased_tickets.append(ticket_serializer.data)

                event_sector = EventSectorPrice.objects.get(event=cart_ticket.event, sector=cart_ticket.sector)

                if event_sector.empty_places > 0:
                    event_sector.empty_places -= 1
                    event_sector.save()
                else:
                    return Response({'error': 'Not enough available places in the sector for the event'})
            else:
                return Response(ticket_serializer.errors)

        cart_tickets.delete()

        return Response({
            'message': 'Tickets successfully purchased',
            'tickets': purchased_tickets
        })


class UserTicketsView(AuthenticatedAPIView, generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.get_user_from_token(self.request)  # Получаем пользователя из токена
        return Ticket.objects.filter(user=user)


class UserCartTicketsView(AuthenticatedAPIView, generics.ListAPIView):
    serializer_class = CartTicketSerializer

    def get_queryset(self):
        user = self.get_user_from_token(self.request)  # Получаем пользователя из токена
        return CartTicket.objects.filter(user=user)


class CreateHallView(AdminAuthenticatedAPIView, generics.CreateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


class CreateSectorView(AdminAuthenticatedAPIView, generics.CreateAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class CreateEventView(AdminAuthenticatedAPIView, generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SetEventSectorPriceView(AdminAuthenticatedAPIView, generics.CreateAPIView):
    queryset = EventSectorPrice.objects.all()
    serializer_class = EventSectorPriceSerializer

class HallListView(APIView):
    def get(self, request):
        halls = Hall.objects.all()
        serializer = HallSerializer(halls, many=True)
        return Response(serializer.data)

class EventListAllView(APIView):
    def get(self, request):
        halls = Event.objects.all()
        serializer = EventSerializer(halls, many=True)
        return Response(serializer.data)

class EventListView(APIView):
    def get(self, request, hall_id):
        events = Event.objects.get(id=hall_id)
        serializer = EventSerializer(events)
        return Response(serializer.data)

class EventSectorListView(APIView):
    def get(self, request, event_id):
        event_sectors = EventSectorPrice.objects.filter(event_id=event_id)
        serializer = EventSectorPriceSerializer(event_sectors, many=True)
        return Response(serializer.data)

class EventSectorDeleteView(APIView):
    def delete(self, request, event_id, sector_id):
        try:
            event_sector = EventSectorPrice.objects.get(event_id=event_id, sector_id=sector_id)
            event_sector.delete()
            return Response({'message': 'Event-sector combination deleted successfully.'})
        except EventSectorPrice.DoesNotExist:
            return Response({'error': 'Event-sector combination not found.'})

class EventDeleteView(APIView):
    def delete(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return Response({'message': 'Event deleted successfully.'})
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'})

class SectorDeleteView(APIView):
    def delete(self, request, sector_id):
        try:
            sector = Sector.objects.get(id=sector_id)
            sector.delete()
            return Response({'message': 'Sector deleted successfully.'})
        except Sector.DoesNotExist:
            return Response({'error': 'Sector not found.'})

class HallDeleteView(APIView):
    def delete(self, request, hall_id):
        try:
            hall = Hall.objects.get(id=hall_id)
            hall.delete()
            return Response({'message': 'Hall deleted successfully.'})
        except Hall.DoesNotExist:
            return Response({'error': 'Hall not found.'})