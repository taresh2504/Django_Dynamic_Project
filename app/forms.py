from django import forms
from .models import User


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'name-box',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'contact', 'address', 'photo', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'name-box', 'placeholder': 'Enter Name'}),
            'email': forms.EmailInput(attrs={'class': 'name-box', 'placeholder': 'Enter Email'}),
            'contact': forms.TextInput(attrs={'class': 'name-box', 'placeholder': 'Enter Contact'}),
            'address': forms.Textarea(attrs={'class': 'address-box', 'placeholder': 'Enter Address'}),
            'photo': forms.FileInput(attrs={'class': 'image-file'}),
            'password': forms.PasswordInput(attrs={'class': 'name-box', 'placeholder': 'Enter Password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        cpwd = cleaned_data.get("confirm_password")

        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data
    
    