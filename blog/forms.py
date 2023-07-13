from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        label="Your Name:",
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. John Wick or Johnny"},
        ),
    )
    email = forms.EmailField(
        label="Your Email:",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "johnwick@example.org"}),
    )
    to = forms.EmailField(
        label="Recipient:",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "oldmarrytodd@example.org"}),
    )
    comments = forms.CharField(
        required=False,
        min_length=10,
        max_length=400,
        label="Comment:",
        disabled=False,
        widget=forms.Textarea(attrs={"placeholder": "What's on your mind?"}),
    )
