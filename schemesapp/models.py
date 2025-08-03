from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserDetails(models.Model):
    GENDER_CHOICES = [
    ('M' ,'Male'),
    ('F' ,'Female'),
    ('T', "Transgender")
    ]

    MARITIAL_CHOICES = [
    ('MARRIED' ,'Married'),
    ('NOT MARRIED' ,'Never Married'),
    ('WIDOWED', "Widowed"),
    ('DIVORCEE', "Divorcee")
    ]

    CASTE_CHOICES = [
    ('G' ,'General'),
    ('OBC' ,'Other Backward Caste(OBC)'),
    ('PVTG', "Particularly Vulnarable Tribal Group"),
    ('SC', "Scheduled Class"),
    ('ST', "Scheduled Tribe")
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    gender= models.CharField(max_length=50, choices=GENDER_CHOICES)
    age = models.IntegerField()
    maritial_status = models.CharField(max_length=50, choices=MARITIAL_CHOICES)
    location = models.CharField(max_length=100, choices=[('rural', "Rural"),('urban', "Urban")])
    caste = models.CharField(max_length=100, choices=CASTE_CHOICES)
    disability = models.BooleanField()
    minority = models.BooleanField()
    below_poverty_line = models.BooleanField()
    income = models.PositiveIntegerField()

class Scheme(models.Model):
    name = models.CharField(max_length=255)
    objective = models.TextField()
    benefits = models.TextField()
    agency = models.CharField(max_length=255)
    full_description = models.TextField(blank=True, null=True) 

    GENDER_CHOICES = [
    ('M' ,'Male'),
    ('F' ,'Female'),
    ('T', "Transgender")
    ]

    MARITIAL_CHOICES = [
    ('MARRIED' ,'Married'),
    ('NOT MARRIED' ,'Never Married'),
    ('WIDOWED', "Widowed"),
    ('DIVORCEE', "Divorcee")
    ]

    CASTE_CHOICES = [
    ('G' ,'General'),
    ('OBC' ,'Other Backward Caste(OBC)'),
    ('PVTG', "Particularly Vulnarable Tribal Group"),
    ('SC', "Scheduled Class"),
    ('ST', "Scheduled Tribe")
    ]

    gender= models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    maritial_status = models.CharField(max_length=50, choices=MARITIAL_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=100, choices=[('rural', "Rural"),('urban', "Urban")], blank=True, null=True)
    caste = models.CharField(max_length=100, choices=CASTE_CHOICES, blank=True, null=True)
    disability = models.BooleanField(blank=True, null=True, default=None)
    minority = models.BooleanField(blank=True, null=True, default=None)
    below_poverty_line = models.BooleanField(blank=True, null=True, default=None)
    max_income = models.PositiveIntegerField(blank=True, null=True, default=None)


    def is_user_eligible(self, details):
        checks = {
        'min_age': lambda: details.age >= self.min_age if self.min_age is not None else True,
        'max_age': lambda: details.age <= self.min_age if self.min_age is not None else True,
        'max_income': lambda: details.income <= self.income if self.income is not None else True,
        'gender': lambda: details.gender.lower() == self.gender.lower() if self.gender else True,
        'caste': lambda: details.caste == self.caste_required if self.caste is not None else True,
        'disability': lambda: details.disability == self.disability if self.disability is not None else True,
        'marital_status': lambda: details.maritial_status == self.maritial_status if self.maritial_status is not None else True,
        'location': lambda: details.location == self.location if self.location is not None else True,
        'minority': lambda: details.minority == self.minority if self.minority is not None else True,
        'below_poverty_line': lambda: details.below_poverty_line == self.below_poverty_line if self.below_poverty_line is not None else 
        True, 
        'max_income': lambda: details.income <= self.max_income if self.max_income is not None else True,
        }
        return all(check() for check in checks.values())

    def __str__(self):
        return self.name

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.TextField(blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username}"
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True,null=True)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - Read: {self.is_read}"

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True)
    _aadhaar =models.BinaryField(db_column='aadhaar_encrypted')

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    @property
    def sensitive_data(self):
        if self._aadhaar:
            return settings.FERNET.decrypt(self._aadhaar).decode()
        return None
    
    @sensitive_data.setter
    def sensitive_data(self, value):
        if value is not None:
            encrypted = settings.FERNET.encrypt(value.encode())
            self._aadhaar = encrypted
        else:
            self._aadhaar = None

