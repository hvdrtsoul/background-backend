from rest_framework import serializers
from .models import Hall, Sector, Event, EventSectorPrice, Ticket, CartTicket


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

class EventSectorPriceSerializer(serializers.ModelSerializer):
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    class Meta:
        model = EventSectorPrice
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    hall_name = serializers.CharField(source='sector.hall', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    class Meta:
        model = Ticket
        fields = '__all__'

class CartTicketSerializer(serializers.ModelSerializer):
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    hall_name = serializers.CharField(source='sector.hall', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    class Meta:
        model = CartTicket
        fields = '__all__'

