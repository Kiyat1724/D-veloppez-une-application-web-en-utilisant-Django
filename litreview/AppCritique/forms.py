from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Ticket, Review


# ======================================================
# MIXIN DE STYLE TAILWIND
# ======================================================

class StyledFormMixin:

    default_classes = (
        "w-full rounded-xl border border-gray-300 "
        "px-4 py-3 text-black bg-white "
        "focus:outline-none focus:ring-2 focus:ring-blue-500"
    )

    def apply_style(self):
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": self.default_classes
            })


# ======================================================
# SIGNUP
# ======================================================

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full p-2 rounded-md text-black bg-white"
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")

        if commit:
            user.save()

        return user

# ======================================================
# TICKET
# ======================================================


class TicketForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

    def clean_image(self):

        image = self.cleaned_data.get(
            'image'
        )

        if image:

            if image.size > 5 * 1024 * 1024:

                raise forms.ValidationError(
                    "L'image ne doit pas dépasser 5 MB."
                )

        return image

# ======================================================
# REVIEW
# ======================================================


class ReviewForm(StyledFormMixin, forms.ModelForm):

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()