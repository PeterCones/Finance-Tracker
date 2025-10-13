from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm
from django.utils.safestring import mark_safe
from django.contrib.auth.password_validation import password_validators_help_text_html


class _StyledFieldsMixin:
    base_input_class = "signin-input form-control glass-input"

    def _style_field(self, name, *, placeholder="", autocomplete=None, autofocus=False, inputmode=None):
        if name not in self.fields:
            return
        field = self.fields[name]
        field.label = ""  # keep labels hidden like your other forms

        # Merge classes
        prev = field.widget.attrs.get("class", "").strip()
        field.widget.attrs["class"] = f"{prev} {self.base_input_class}".strip()

        if placeholder:
            field.widget.attrs["placeholder"] = placeholder
        if autocomplete:
            field.widget.attrs["autocomplete"] = autocomplete
        if inputmode:
            field.widget.attrs["inputmode"] = inputmode
        if autofocus:
            field.widget.attrs["autofocus"] = "autofocus"


class CustomLoginForm(_StyledFieldsMixin, LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allauth "login" can be username or email depending on settings
        self._style_field("login", placeholder="Username or Email", autocomplete="username", autofocus=True)
        self._style_field("password", placeholder="Password", autocomplete="current-password")


class CustomSignupForm(_StyledFieldsMixin, SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_field("username",  placeholder="Username", autocomplete="username", autofocus=True)
        self._style_field("email",     placeholder="Email",    autocomplete="email",    inputmode="email")
        self._style_field("password1", placeholder="Password", autocomplete="new-password")
        self._style_field("password2", placeholder="Confirm Password", autocomplete="new-password")

        # Add budget_heading to each bullet in the password help
        try:
            help_html = password_validators_help_text_html() or ""
            help_html = help_html.replace("<ul>", '<ul class="password-rules">')
            help_html = help_html.replace("<li>", '<li class="budget_heading">')
            self.fields["password1"].help_text = mark_safe(help_html)
        except Exception:
            pass  # fall back to default help


class CustomPasswordForm(_StyledFieldsMixin, ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_field("email", placeholder="Enter your email", autocomplete="email", inputmode="email")