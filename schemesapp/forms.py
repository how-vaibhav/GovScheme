from django import forms
from django.contrib.auth.models import User
from .models import Feedback, Scheme, UserDetails


# =========================
# SHARED TAILWIND STYLES
# =========================

BASE_INPUT = """
w-full px-4 py-3 rounded-xl
bg-gray-50 dark:bg-gray-800
border border-gray-300 dark:border-gray-700
text-gray-900 dark:text-gray-100
focus:outline-none focus:ring-4
focus:ring-primary-200 dark:focus:ring-primary-800/40
focus:border-primary-500
transition duration-200
"""

SEGMENTED_OPTION = """
peer hidden
"""

SEGMENTED_LABEL = """
flex items-center justify-center
px-4 py-3 rounded-xl
border border-gray-300 dark:border-gray-700
bg-gray-50 dark:bg-gray-800
cursor-pointer
transition
peer-checked:bg-primary-600
peer-checked:text-white
peer-checked:border-primary-600
hover:border-primary-500
text-sm font-medium
"""


# =========================
# FEEDBACK FORM
# =========================

class FeedbackForm(forms.ModelForm):

    scheme = forms.ModelChoiceField(
        queryset=Scheme.objects.all(),
        required=False,
        empty_label="Select a Scheme",
        widget=forms.Select(attrs={'class': BASE_INPUT})
    )

    class Meta:
        model = Feedback
        fields = ['scheme', 'message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': BASE_INPUT,
                'rows': 4
            })
        }


class AddEmployee(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Enter Username",
        widget=forms.TextInput(attrs={
            'class': BASE_INPUT,
            'placeholder': 'Employee username'
        })
    )


class Add_Scheme_Form(forms.ModelForm):

    class Meta:
        model = Scheme
        fields = [
            'name',
            'objective',
            'benefits',
            'agency',
            'full_description',
            'category',
            'website',
            'contact_email',
            'contact_phone',
            'application_deadline',
            'gender',
            'min_age',
            'max_age',
            'maritial_status',
            'location',
            'caste',
            'disability',
            'minority',
            'below_poverty_line',
            'max_income',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': BASE_INPUT}),
            'objective': forms.Textarea(attrs={'class': BASE_INPUT, 'rows': 3}),
            'benefits': forms.Textarea(attrs={'class': BASE_INPUT, 'rows': 3}),
            'agency': forms.TextInput(attrs={'class': BASE_INPUT}),
            'full_description': forms.Textarea(attrs={'class': BASE_INPUT, 'rows': 4}),
            'category': forms.Select(attrs={'class': BASE_INPUT}),
            'website': forms.URLInput(attrs={'class': BASE_INPUT}),
            'contact_email': forms.EmailInput(attrs={'class': BASE_INPUT}),
            'contact_phone': forms.TextInput(attrs={'class': BASE_INPUT}),
            'application_deadline': forms.DateInput(attrs={'class': BASE_INPUT, 'type': 'date'}),
            'gender': forms.Select(attrs={'class': BASE_INPUT}),
            'min_age': forms.NumberInput(attrs={'class': BASE_INPUT}),
            'max_age': forms.NumberInput(attrs={'class': BASE_INPUT}),
            'maritial_status': forms.Select(attrs={'class': BASE_INPUT}),
            'location': forms.Select(attrs={'class': BASE_INPUT}),
            'caste': forms.Select(attrs={'class': BASE_INPUT}),
            'disability': forms.Select(attrs={'class': BASE_INPUT}),
            'minority': forms.Select(attrs={'class': BASE_INPUT}),
            'below_poverty_line': forms.Select(attrs={'class': BASE_INPUT}),
            'max_income': forms.NumberInput(attrs={'class': BASE_INPUT}),
        }


# =========================
# USER DETAILS FORM
# =========================

YES_NO_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No')
]


class User_Details_Form(forms.ModelForm):

    gender = forms.ChoiceField(
        choices=[
            ('M', 'Male'),
            ('F', 'Female')
        ],
        widget=forms.RadioSelect
    )

    disability = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect
    )

    minority = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect
    )

    below_poverty_line = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = UserDetails
        fields = [
            'name',
            'age',
            'email',
            'gender',
            'maritial_status',
            'location',
            'caste',
            'disability',
            'minority',
            'below_poverty_line',
            'income'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': BASE_INPUT,
                'placeholder': 'Full Name'
            }),
            'age': forms.Select(attrs={'class': BASE_INPUT}),
            'email': forms.EmailInput(attrs={
                'class': BASE_INPUT,
                'placeholder': 'your@email.com'
            }),
            'maritial_status': forms.Select(attrs={'class': BASE_INPUT}),
            'location': forms.Select(attrs={'class': BASE_INPUT}),
            'caste': forms.Select(attrs={'class': BASE_INPUT}),
            'income': forms.NumberInput(attrs={
                'class': BASE_INPUT,
                'placeholder': 'Annual income in INR'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.initial['disability'] = 'yes' if self.instance.disability else 'no'
            self.initial['minority'] = 'yes' if self.instance.minority else 'no'
            self.initial['below_poverty_line'] = 'yes' if self.instance.below_poverty_line else 'no'

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

    def clean_disability(self):
        return self.cleaned_data.get('disability') == 'yes'

    def clean_minority(self):
        return self.cleaned_data.get('minority') == 'yes'

    def clean_below_poverty_line(self):
        return self.cleaned_data.get('below_poverty_line') == 'yes'