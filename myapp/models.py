from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Customer(models.Model):
    name = models.CharField(max_length=32)
    number = models.TextField(max_length=13)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # location = models.CharField(max_length=13, unique=True)
    age = models.IntegerField()
    email = models.TextField(max_length=32)
    gender = models.CharField(max_length=10)
    address = models.TextField(max_length=255)
    
    def __str__(self):
        return self.name


class Phlabo(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Phlabo', 'Phlabo'),
        ('Super Admin', 'Super Admin'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('disable', 'Disable'),
    ]

    name = models.CharField(max_length=32)
    number = models.CharField(max_length=13)
    email = models.CharField(max_length=32)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='Phlabo')
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

# class Custest(models.Model):
#     testList = models.ar
#     rate = 
#     code = 


class Tests(models.Model):
    testName = models.TextField(max_length=64)
    testCode = models.TextField(max_length=16)
    price = models.FloatField()



# models.FloatField(
#         null=False,
#         blank=False,
#         default=0.0,
#         validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
#         help_text="Enter the price of the test between 0 and 10000",
#         verbose_name="Test Price"
#     )

class Booking(models.Model):
    VISIT_TYPE_CHOICES = [
        ('home', 'Home Visit'),
        ('lab', 'Lab Visit'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    phlabo = models.ForeignKey(Phlabo, on_delete=models.CASCADE)
    tests = models.ManyToManyField(Tests)
    booking_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    visit_type = models.CharField(
        max_length=4,
        choices=VISIT_TYPE_CHOICES,
        default='lab'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking {self.id} by {self.customer}"