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
        required=False,
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

    age = forms.CharField(
        widget=forms.Select(
            choices=AGE_CHOICES,
            attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
            }
        ),
        help_text='Select your age group',
        required=True,
    )

    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female')],
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none'
        })
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
            'disability': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500'
            }),
            'minority': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500'
            }),
            'below_poverty_line': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500'
            }),
            'income': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all outline-none',
                'placeholder': 'Annual income in INR'
            }),
        }

    def clean_age(self):
        age_value = (self.cleaned_data.get('age') or '').strip()
        valid_ranges = {choice[0] for choice in UserDetails.AGE_CHOICES}

        if age_value in valid_ranges:
            return age_value

        if age_value.isdigit():
            numeric_age = int(age_value)
            if 18 <= numeric_age <= 25:
                return '18-25'
            if 26 <= numeric_age <= 35:
                return '26-35'
            if 36 <= numeric_age <= 45:
                return '36-45'
            if 46 <= numeric_age <= 55:
                return '46-55'
            if 56 <= numeric_age <= 65:
                return '56-65'
            if numeric_age >= 66:
                return '65+'

        raise forms.ValidationError('Please select a valid age group.')