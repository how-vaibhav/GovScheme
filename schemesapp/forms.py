from django import forms
from django.contrib.auth.models import User
from .models import Feedback, Scheme, UserDetails

# Predefined choices for common fields
AGE_CHOICES = [
    ('', 'Select Age'),
    ('18-25', '18-25 years'),
    ('26-35', '26-35 years'),
    ('36-45', '36-45 years'),
    ('46-55', '46-55 years'),
    ('56-65', '56-65 years'),
    ('65+', '65 years and above'),
]

AGE_RANGE_CHOICES = [
    ('', 'Any Age'),
] + [(str(i), str(i)) for i in range(18, 76)]

INCOME_RANGE_CHOICES = [
    ('', 'Any Income'),
    ('0-100000', '₹0 - ₹1 Lakh'),
    ('100000-300000', '₹1 Lakh - ₹3 Lakh'),
    ('300000-500000', '₹3 Lakh - ₹5 Lakh'),
    ('500000-1000000', '₹5 Lakh - ₹10 Lakh'),
    ('1000000+', 'Above ₹10 Lakh'),
]

LOCATION_CHOICES = [
    ('', 'Any Location'),
    ('rural', 'Rural'),
    ('urban', 'Urban'),
]

YES_NO_CHOICES = [
    ('', 'Select'),
    ('true', 'Yes'),
    ('false', 'No'),
]

class FeedbackForm(forms.ModelForm):

    scheme = forms.ModelChoiceField(
        queryset=Scheme.objects.all(), 
        empty_label="Select a Scheme", 
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
        })
    )

    class Meta:
        model = Feedback
        fields = ['scheme', 'message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none',
                'rows': 4
            })
        }

class AddEmployee(forms.Form):
    username = forms.CharField(
        max_length=150, 
        label="Enter Username",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
        })
    )

class Add_Scheme_Form(forms.ModelForm):

    class Meta:
        model = Scheme
        fields = ['name', 'objective', 'benefits', 'agency', 'full_description', 'gender', 'min_age', 'max_age', 'maritial_status', 'location', 'caste', 'disability', 'minority', 'below_poverty_line', 'max_income' ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'objective': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none',
                'rows': 3
            }),
            'benefits': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none',
                'rows': 3
            }),
            'agency': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none',
                'rows': 4
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'min_age': forms.Select(choices=AGE_RANGE_CHOICES, attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'max_age': forms.Select(choices=AGE_RANGE_CHOICES, attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'maritial_status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'location': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'caste': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'disability': forms.Select(choices=[(None, 'Any'), (True, 'Yes'), (False, 'No')], attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'minority': forms.Select(choices=[(None, 'Any'), (True, 'Yes'), (False, 'No')], attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'below_poverty_line': forms.Select(choices=[(None, 'Any'), (True, 'Yes'), (False, 'No')], attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'max_income': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none',
                'placeholder': 'Maximum income limit'
            }),
        }

class User_Details_Form(forms.ModelForm):
    
    age = forms.ChoiceField(
        choices=AGE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
        }),
        help_text='Select your age group'
    )

    class Meta:
        model = UserDetails
        fields = ['name', 'age', 'email', 'gender', 'maritial_status', 'location', 'caste', 'disability', 'minority', 'below_poverty_line', 'income' ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none',
                'placeholder': 'your@email.com'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'maritial_status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'location': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'caste': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'disability': forms.Select(choices=YES_NO_CHOICES, attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'minority': forms.Select(choices=YES_NO_CHOICES, attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'below_poverty_line': forms.Select(choices=YES_NO_CHOICES, attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }),
            'income': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none',
                'placeholder': 'Annual income in INR'
            }),
        }