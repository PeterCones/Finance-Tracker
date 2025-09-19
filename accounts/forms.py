from allauth.account.forms import LoginForm


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'placeholder': 'Email address'})
        self.fields['login'].label = ""
        self.fields['login'].widget.attrs.update({'class': 'signin-input'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password'].label = ""
        self.fields['password'].widget.attrs.update({'class': 'signin-input'})