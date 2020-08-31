from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

# Create your forms here. This specific form makes a direct reference to a model in the app.
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0) #define form inputs for stuff you are hiding because your model expects an input for those attributes
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0) #if you excluded these hidden inputs in the meta, it should work as well
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    #link the model and the form
    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Enter page title.")
    url = forms.URLField(max_length=200,help_text="Enter URL of page.")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    def clean(self):

        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data

    #link the model and the form
    class Meta:
        model = Page
        #fields = ('title', 'url', 'category',)
        exclude = ('category',) #specify what to exclude for form inputs

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        url = cleaned_data.get('website')
        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['website'] = url
            return cleaned_data
            
    class Meta:
        model = UserProfile
        fields = ('website' , 'picture')

