from django.forms import ModelForm, Form
from .models import Users, User_details, Post
from django import forms
from django.contrib.auth.forms import UserCreationForm



# define the class of a form
class RegistrationForm1(ModelForm):
    class Meta:
        # write the name of models for which the form is made
        model = User_details

        # Custom fields
        fields = ["first_name", "last_name", "age", "gender", "address", "user_id"]

    # this function will be used for the validation
    def clean(self):

        # data from the form is fetched using super function
        super(RegistrationForm1, self).clean()

        # extract the first_name from the data
        first_name = self.cleaned_data.get('first_name')
        age = self.cleaned_data.get('age')

        # conditions to be met for the first_name length
        if len(first_name) < 3:
            self._errors['first_name'] = self.error_class([
                'Minimum 3 characters required'])
        if age == 0:
            self.errors['age'] = self.error_class([
                'age cannot be 0'])

        # return any errors if found
        return self.cleaned_data


class RegistrationForm2(UserCreationForm):
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    class Meta:
        # write the name of models for which the form is made
        model = Users

        # Custom fields
        fields = ["username","email", "phone_number"]


class LogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class PostForm(ModelForm):
    #user_id = forms.ModelChoiceField(queryset=Users.objects.filter())
    class Meta:
        model = Post

        fields = ["blog_title", "post_here"]
        exclude = ["user"]




