# quiz/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# ----------------------------
# User Registration Form
# ----------------------------
class RegisterForm(UserCreationForm):
    """
    Extended registration form with email field.
    Inherits password hashing from UserCreationForm.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class':       'form-control',
            'placeholder': 'Enter your email',
        })
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']

    # Apply Bootstrap classes to all fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class':       'form-control',
            'placeholder': 'Choose a username',
        })
        self.fields['password1'].widget.attrs.update({
            'class':       'form-control',
            'placeholder': 'Create password',
        })
        self.fields['password2'].widget.attrs.update({
            'class':       'form-control',
            'placeholder': 'Confirm password',
        })

        # Clean up default Django help texts
        self.fields['username'].help_text = 'Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Minimum 8 characters.'
        self.fields['password2'].help_text = ''

    def clean_email(self):
        """Ensure email is unique across all users."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


# ----------------------------
# User Login Form
# ----------------------------
class LoginForm(AuthenticationForm):
    """
    Custom login form with Bootstrap styling.
    Inherits authentication logic from AuthenticationForm.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class':       'form-control',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class':       'form-control',
            'placeholder': 'Password',
        })
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'