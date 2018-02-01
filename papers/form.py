from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from papers.models import Paper, Author, CustomUser, PaperRequests, PCM, Reviews
from django.forms.models import ModelForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email", max_length=30)
    password = forms.CharField(label="Password", max_length=30, min_length=8, widget=forms.PasswordInput())

    class Meta:
        model = Author


class AuthorCreationForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ['username', 'first_name', 'last_name', 'street_line_1', 'street_line_2', 'city', 'state', 'zip_code',
                  'phone_number']

    def save(self, commit=True):
        user = super(AuthorCreationForm, self).save(commit=False)
        # copy the submitted cleaned form-data to the user's properties
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.street_line_1 = self.cleaned_data["street_line_1"]
        user.street_line_2 = self.cleaned_data["street_line_2"]
        user.city = self.cleaned_data["city"]
        user.state = self.cleaned_data["state"]
        user.zip_code = self.cleaned_data["zip_code"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.user_type = 0
        if commit:
            user.save()
        return user


class PaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = ['file', 'title', 'abstract']

    def validate_file_extension(self):
        import os
        ext = os.path.splitext(self.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if not ext in valid_extensions:
            raise forms.ValidationError('File extension not supported! '
                                        'Please submit your paper in .doc, .docx or .pdf format.')

    file = forms.FileField(validators=[validate_file_extension])

    def save(self, commit=True):
        paper = super(PaperForm, self).save(commit=False)
        if commit:
            paper.save()
        return paper


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'street_line_1', 'street_line_2', 'city', 'state', 'zip_code',
                  'phone_number']

    def save(self, commit=True):
        user = super(ProfileUpdateForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class PostForm(forms.Form):
    def is_request(self):
        return 'request' in self.data

    def is_cancel(self):
        return 'cancel' in self.data

class ReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['comment', 'rate']

    def save(self, commit=True):
        review = super(ReviewForm, self).save(commit=False)
        if commit:
            review.save()
        return review

class AssignForm(ModelForm):

    class Meta:
        model = Paper
        fields=['pcm_one','pcm_two','pcm_three']

    # def __init__(self, *args, **kwargs):
    #     super(AssignForm, self).__init__(*args, **kwargs)
    #     self.fields['pcm_one'] = forms.ChoiceField(
    #         choices= PaperAssigned.assign_papers(self))
    #     self.fields['pcm_two'] = forms.ChoiceField(
    #         choices= PaperAssigned.assign_papers(self))
    #     self.fields['pcm_three'] = forms.ChoiceField(
    #         choices= PaperAssigned.assign_papers(self))

    def save(self, commit=True):
        assign = super(AssignForm, self).save(commit=False)
        if commit:
            assign.save()
        return assign

class RateForm(ModelForm):
    class Meta:
        model = Paper
        fields = ['rate']

    def save(self, commit=True):
        rate = super(RateForm, self).save(commit=False)
        if commit:
            rate.save()
        return rate

