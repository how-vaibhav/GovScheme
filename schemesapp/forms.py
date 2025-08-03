from django import forms
from django.contrib.auth.models import User
from .models import Feedback, Scheme, UserDetails

class FeedbackForm(forms.ModelForm):

    scheme = forms.ModelChoiceField(queryset=Scheme.objects.all(), empty_label="Select a Scheme", widget=forms.Select(attrs={'class': 'form_control'}))

    class Meta:
        model = Feedback
        fields = ['scheme', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form_control', 'rows': 4})
        }

class AddEmployee(forms.Form):
    username = forms.CharField(max_length=150, label="Enter Username")

class Add_Scheme_Form(forms.ModelForm):

    class Meta:
        model = Scheme
        fields = ['name', 'objective', 'benefits', 'agency', 'full_description', 'gender', 'min_age', 'max_age', 'maritial_status', 'location', 'caste', 'disability', 'minority', 'below_poverty_line', 'max_income' ]
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'maritial_status': forms.Select(attrs={'class': 'form-control'}),
            'caste': forms.Select(attrs={'class': 'form-control'}),
        }

class User_Details_Form(forms.ModelForm):

    class Meta:
        model = UserDetails
        fields = ['name', 'age', 'email', 'gender', 'maritial_status', 'location', 'caste', 'disability', 'minority', 'below_poverty_line', 'income' ]
        widgets = {
                'gender': forms.Select(attrs={'class': 'form-control'}),
                'maritial_status': forms.Select(attrs={'class': 'form-control'}),
                'caste': forms.Select(attrs={'class': 'form-control'}),
                'disability': forms.Select(choices=[(True, 'Yes'), (False, 'No')]),
                'minority': forms.Select(choices=[(True, 'Yes'), (False, 'No')]),
                'below_poverty_line': forms.Select(choices=[(True, 'Yes'), (False, 'No')]),
            }