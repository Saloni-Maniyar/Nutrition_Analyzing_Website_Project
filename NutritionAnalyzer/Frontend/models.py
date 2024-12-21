# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# # Create your models here.


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         """
#         Creates and returns a regular user with an email and password.
#         """
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser):
#     GENDER_CHOICES = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Other', 'Other'),
#     ]
    
#     ACTIVITY_LEVEL_CHOICES = [
#         ('Sedentary', 'Little or no exercise, sitting most of the day'),
#         ('Lightly Active', 'Light exercise or sports 1-3 days per week'),
#         ('Moderately Active', 'Moderate exercise or sports 3-5 days per week'),
#         ('Very Active', 'Hard exercise or sports 6-7 days per week'),
#     ]

#     # Define the fields
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)  # Store password (hashed later)
#     name = models.CharField(max_length=50)
#     age = models.PositiveIntegerField()  # Age should be an integer between 10 and 100
#     weight = models.PositiveIntegerField()  # Weight should be a number between 20 and 200
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
#     activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    
#     # Optional: Add date of registration
#     registration_date = models.DateTimeField(auto_now_add=True)

#     # Fields inherited from AbstractBaseUser
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     last_login = models.DateTimeField(auto_now=True)

#     # Add related_name to avoid reverse access issues
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='accounts_user_set',  # Added related_name
#         blank=True,
#         help_text='The groups this user belongs to.',
#         verbose_name='groups'
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='accounts_user_permissions_set',  # Added related_name
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions'
#     )

#     # Specify email as the username field for authentication
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']  # Add any other fields you want to be mandatory

#     # Custom manager for handling user creation
#     objects = CustomUserManager()

#     def __str__(self):
#         return f'{self.name} ({self.email})'

#     # Custom validation for age and weight
#     def clean(self):
#         if self.age < 10 or self.age > 100:
#             raise models.ValidationError("Age must be between 10 and 100.")
#         if self.weight < 20 or self.weight > 200:
#             raise models.ValidationError("Weight must be between 20 and 200 kg.")
#         super().clean()  # Call parent clean() method
 
 
 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# User model
class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('Sedentary', 'Little or no exercise, sitting most of the day'),
        ('Lightly Active', 'Light exercise or sports 1-3 days per week'),
        ('Moderately Active', 'Moderate exercise or sports 3-5 days per week'),
        ('Very Active', 'Hard exercise or sports 6-7 days per week'),
    ]

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store password (hashed later)
    name = models.CharField(max_length=50)

    # These fields should be optional for superusers
    age = models.PositiveIntegerField(null=True, blank=True)  # Optional for superusers
    weight = models.PositiveIntegerField(null=True, blank=True)  # Optional for superusers
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)  # Optional for superusers
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, null=True, blank=True)  # Optional for superusers
    
    registration_date = models.DateTimeField(auto_now_add=True)

    # Fields inherited from AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    # Add related_name to avoid reverse access issues
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Add any other fields you want to be mandatory

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name} ({self.email})'

    # Custom validation for age and weight
    def clean(self):
        if self.age and (self.age < 10 or self.age > 100):
            raise models.ValidationError("Age must be between 10 and 100.")
        if self.weight and (self.weight < 20 or self.weight > 200):
            raise models.ValidationError("Weight must be between 20 and 200 kg.")
        super().clean()  # Call parent clean() method



#for Analyzed data 
class NutritionAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    fiber = models.FloatField()
    sugars = models.FloatField()
    sodium = models.FloatField()
    cholesterol = models.FloatField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} - {self.user.name}"