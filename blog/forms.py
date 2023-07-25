from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        label="Your Name:",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. John Wick or Johnny",
                "size": "26",
            },
        ),
    )
    email = forms.EmailField(
        label="Your Email:",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "johnwick@example.org",
                "size": "26",
            }
        ),
    )
    to = forms.EmailField(
        label="Recipient:",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "oldmarrytodd@example.org",
                "size": "26",
            }
        ),
    )
    comments = forms.CharField(
        required=False,
        min_length=10,
        max_length=400,
        label="Comment:",
        disabled=False,
        widget=forms.Textarea(attrs={"placeholder": "What's on your mind?"}),
    )


class CommentForm(forms.ModelForm):
    """Form definition for Comment."""

    class Meta:
        """Meta definition for a comment form."""

        model = Comment
        fields = (
            "name",
            "email",
            "body",
        )
