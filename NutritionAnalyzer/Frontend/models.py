from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import pytz  # To use timezones



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

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

    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, null=True, blank=True)

    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

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
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name} ({self.email})'

    def clean(self):
        if self.age and (self.age < 10 or self.age > 100):
            raise models.ValidationError("Age must be between 10 and 100.")
        if self.weight and (self.weight < 20 or self.weight > 200):
            raise models.ValidationError("Weight must be between 20 and 200 kg.")
        if self.height and (self.height < 50 or self.height > 250):
            raise models.ValidationError("Height must be between 50 and 250 cm.")
        super().clean()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

# Nutrition Analysis Model
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

    # Class method to get today's data for a user
    @classmethod
    def get_today_data(cls, user):
        # Convert timezone-aware datetime to 'Asia/Kolkata' timezone
        kolkata_tz = pytz.timezone('Asia/Kolkata')
        today_start = timezone.now().astimezone(kolkata_tz).replace(hour=0, minute=0, second=0, microsecond=0)  # Midnight start of today
        today_end = today_start.replace(hour=23, minute=59, second=59, microsecond=999999)  # End of the day (just before midnight)

        # Fetch records for today within the range (ignoring the time portion)
        return cls.objects.filter(user=user, analyzed_at__gte=today_start, analyzed_at__lt=today_end)

