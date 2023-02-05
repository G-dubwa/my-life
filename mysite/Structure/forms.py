from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import Priority,Element,Aspect, Financial_Entity,Entity_Amount,Entity_Aspect, Event
from django import forms
from django.forms import ModelForm
# Create your forms here.
from django.contrib.auth import get_user_model

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model =  get_user_model()
		fields = ("email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class PriorityUploadForm(ModelForm):
	priority_name = forms.TextInput()
	image = forms.ImageField()
	class Meta:
		model = Priority
		fields = ['priority_name', 'description', 'significance','image']
		

class ElementUploadForm(ModelForm):
	element_name = forms.TextInput()
	image = forms.ImageField()
	class Meta:
		model = Element
		fields = ['element_name', 'description', 'element_type','significance','image']

class AspectUploadForm(ModelForm):
	aspect_name = forms.TextInput()
	image = forms.ImageField()
	class Meta:
		model = Aspect
		fields = ['aspect_name', 'description','significance','image']

class AspectEditForm(ModelForm):
	class Meta:
		model = Aspect
		fields = ['aspect_name', 'description','significance','completion','image']



class ChangeEmail(forms.Form):
	email = forms.EmailField(required=True,help_text="Enter new email.")
	def clean_new_email(self):
		data = self.cleaned_data['email']
		return data

class EntityUploadForm(ModelForm):
	class Meta:
		model = Financial_Entity
		fields = ['name', 'description','image','active']
		

class FinAspectUploadForm(ModelForm):

	class Meta:
		model = Entity_Aspect
		fields = ['name', 'description','image','active']

class UpdateUploadForm(ModelForm):
	class Meta:
		model = Entity_Amount
		fields = ['amount']

class EventUploadForm(ModelForm):
	date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
	class Meta:
		model=Event
		fields=['title','description','date']