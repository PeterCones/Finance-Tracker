from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from allauth.account.forms import ResetPasswordForm

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'placeholder': 'Email address'})
        self.fields['login'].label = ""
        self.fields['login'].widget.attrs.update({'class': 'signin-input'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password'].label = ""
        self.fields['password'].widget.attrs.update({'class': 'signin-input'})
        
class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['username'].widget.attrs.update({'class': 'signin-input'})
        self.fields['username'].label = ""
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['email'].widget.attrs.update({'class': 'signin-input'})
        self.fields['email'].label = ""
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password1'].widget.attrs.update({'class': 'signin-input'})
        self.fields['password1'].label = ""
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        self.fields['password2'].widget.attrs.update({'class': 'signin-input' })
        self.fields['password2'].label = ""

class CustomPasswordForm(ResetPasswordForm):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['email'].label = ""
        self.fields['email'].widget.attrs.update({'class': 'signin-input' })