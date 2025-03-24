from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }
        help_texts = {
            'username': None,    # Remove username help text
            'password1': None,   # Remove password1 help text
            'password2': None,   # Remove password2 help text
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2


from django import forms

# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )


from django import forms
from .models import ImageUpload

# Image Upload Form
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image', 'image_name', 'subject']
        widgets = {
            'image_name': forms.TextInput(attrs={'placeholder': 'Image Name', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
        }

from django import forms

# Email Form
class EmailForm(forms.Form):
    username = forms.CharField(label="Recipient Username", widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    subject = forms.CharField(label="Subject", widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}))


from django import forms

class PasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter QR Code Password'}),
        label='Password'
    )





from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image','image_name']


# forms.py
# myapp/forms.py
from django import forms

class ProfileForm(forms.Form):
    # Define your fields here
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    # Add other fields as needed




from django import forms
from .models import SentEmail

class SentEmailForm(forms.ModelForm):
    class Meta:
        model = SentEmail
        fields = ['recipient_email', 'secret_key', 'image']
