from django.db import models

class Customer(models.Model):
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Phone_number = models.CharField(max_length=15)
    Email = models.EmailField()
    Password = models.CharField(max_length=500)


    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
           return Customer.objects.get(Email=email)
        except:
            return False

    def isExists(self):
        if Customer.objects.filter(Email=self.Email):
            return True
        return False