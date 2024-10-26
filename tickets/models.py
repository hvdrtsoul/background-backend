from django.db import models
from users.models import User

# Create your models here.
class Hall(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(max_length=255)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='sectors')
    seat_count = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.hall.name}'


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    sectors_image = models.ImageField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='events')
    date = models.DateTimeField()

    def __str__(self):
        return self.name


class EventSectorPrice(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_sector_prices')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='event_sector_prices')
    price = models.IntegerField()
    empty_places = models.IntegerField()

    class Meta:
        unique_together = ('event', 'sector')

    def __str__(self):
        return f'{self.event.name} - {self.sector.name}'


class Ticket(models.Model):
    owner_first_name = models.CharField(max_length=255)
    owner_last_name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    price = models.IntegerField()
    def __str__(self):
        return f'Ticket for {self.event.name} in {self.sector.name} (Owner: {self.owner_first_name} {self.owner_last_name})'

class CartTicket(models.Model):
    owner_first_name = models.CharField(max_length=255)
    owner_last_name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='cart_tickets')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='cart_tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_tickets')
    price = models.IntegerField()

    def __str__(self):
        return f'Cart ticket for {self.event.name} in {self.sector.name} (Owner: {self.owner_first_name} {self.owner_last_name})'
