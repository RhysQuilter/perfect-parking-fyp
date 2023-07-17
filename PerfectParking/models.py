from geopy.distance import geodesic
from django.db import models

# Create your models here.
class ParkingLot(models.Model):
    """
    A model representing a parking lot.

    Attributes:
        id (int): The primary key of the parking lot.
        name (str): The name of the parking lot (max length 100).
        address (str): The address of the parking lot (max length 255).
        hours (str): The operating hours of the parking lot (max length 255).
        isPaidParking (bool): Whether the parking lot requires payment or not (default True).
        latitude (Decimal): The latitude of the parking lot location (max digits 17, decimal places 15).
        longitude (Decimal): The longitude of the parking lot location (max digits 17, decimal places 15).
        image (ImageField): An optional image of the parking lot (uploaded to 'images/parking-lot/').
        parking_spaces (int): The number of parking spaces available (default 1).

    Methods:
        __str__(): Returns the name of the parking lot as a string.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    hours = models.CharField(max_length=255)
    isPaidParking = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=17, decimal_places=15)
    image = models.ImageField(upload_to='images/parking-lot/', blank=True)
    parking_spaces = models.IntegerField(default=1)
    
    def __str__(self):
        return self.name
    
class ParkingLotMonitor(models.Model):
    """
    A model representing a parking lot monitor.

    Attributes:
        id (int): The primary key of the parking lot monitor.
        parkingLot (ForeignKey): A foreign key to the ParkingLot that this monitor is associated with.
        name (str): The name of the parking lot monitor (max length 100).
        latitude (Decimal): The latitude of the parking lot monitor location (max digits 17, decimal places 15).
        longitude (Decimal): The longitude of the parking lot monitor location (max digits 17, decimal places 15).
        probabilityParkingAvailable (Decimal): The probability that the parking lot is available (max digits 5, decimal places 2, default 0).
        free_parking_spaces (int): The number of free parking spaces available (default 0).
        dateTimeLastUpdated (DateTimeField): The date and time when the monitor was last updated (auto_now=True).
        status (bool): Whether the monitor is currently online or offline (default True).
        image (ImageField): An optional image of the parking lot monitor (uploaded to 'images/parking-lot-monitor/').

    Methods:
        None.
    """
    id = models.AutoField(primary_key=True)
    parkingLot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    """The name of the parking lot monitor.
    This is the name that will be displayed to the user.
    Max length is 100 characters."""
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    """The latitude of the parking lot monitor"""
    longitude = models.DecimalField(max_digits=17, decimal_places=15)
    """The longitude of the parking lot monitor"""
    probabilityParkingAvailable = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    """The probability that the parking lot is available."""
    free_parking_spaces = models.IntegerField(default=0)
    dateTimeLastUpdated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    """status: True = online, False = offline"""
    image = models.ImageField(upload_to='images/parking-lot-monitor/', blank=True)
    
    def get_distance_from_lat_lang(self, latitude, longitude) -> float:
        """Calculates the distance between the current object and a point specified by latitude and longitude.

        Args:
            latitude (float): The latitude of the point in degrees.
            longitude (float): The longitude of the point in degrees.

        Returns:
            float: The distance between the current object and the specified point in kilometers.

        Raises:
            None.
        """
        point:tuple = (latitude, longitude)
        return self.get_distance_from_point(point)
    
    def get_distance_from_point(self, user_point: tuple) -> float:
        """Gets the distance in Kilometers from the user GPS coordinates to the parking lot coordinates.

        Returns:
            float: The distance in Kilometers from the user GPS coordinates to the parking lot coordinates.
        """
        return round(geodesic(self.get_gps_point(), user_point).km, 2)

    
    def get_gps_point(self) -> tuple:
        """Gets the GPS coordinates of the parking lot.

        Returns:
            tuple: The GPS coordinates of the parking lot.
        """
        return (self.latitude, self.longitude)
    
    def __str__(self):
        return self.name
