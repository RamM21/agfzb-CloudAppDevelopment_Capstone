from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.name + \
               self.description



# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    dealerid = models.IntegerField()
    SEDAN = 'Sedan'
    SUV = 'Suv'
    WAGON = 'Wagon'
    MODEL_MODES=[
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon')
    ]
    type = models.CharField(max_length=10, choices=MODEL_MODES,default=SEDAN)
    year = models.DateField()

    def __str__(self):
        return self.name +","+\
               self.type
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review):
        self.make = ""
        self.car_model = ""
        self.car_year = ""
        self.dealership = dealership
        self.id = ""  # The id of the review
        self.name = name  # Name of the reviewer
        self.purchase = purchase  # Did the reviewer purchase the car? bool
        self.purchase_date = ""
        self.review = review  # The actual review text
        self.sentiment = ""  # Watson NLU sentiment analysis of review

    def __str__(self):
        return "Reviewer: " + self.name + " Review: " + self.review
