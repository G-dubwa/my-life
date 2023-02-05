from django.shortcuts import render, redirect
from django.template import loader
# Create your views here.
import os
from django.urls import reverse
from django.http import HttpResponse
from .models import Priority,Element,Aspect, Financial_Entity,Entity_Amount,Entity_Aspect,Event
#from django.contrib.auth.models import User
from django.http import Http404
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import PriorityUploadForm, ElementUploadForm, AspectUploadForm, AspectEditForm, ChangeEmail, EntityUploadForm,FinAspectUploadForm,UpdateUploadForm,EventUploadForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.contrib.auth import get_user_model
User = get_user_model()
def delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)
class EmailThread(threading.Thread):
	def __init__(self, email):
		self.email=email
		threading.Thread.__init__(self)
	def run(self):
		self.email.send()
def send_activation_email(user, request):
	current_site = get_current_site(request)
	email_subject = 'Activate your account'
	email_body = render_to_string('Structure/authenticate/activate.html',{'user':user,'domain':current_site,'uid':urlsafe_base64_encode(force_bytes(user.pk)),'token':generate_token.make_token(user)})
	email = EmailMessage(subject=email_subject,body=email_body,from_email=settings.EMAIL_FROM_USER, to=[user.email])
	EmailThread(email).start()
def index(request):
    '''latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)'''
    return render(request,'Structure/index.html')

def priority(request, question_id):
    try:
        question = Priority.objects.get(pk=question_id)
    except Priority.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'Structure/priority.html', {'question': question})

def register_request(request):
	if request.method == "POST":
		print(request.POST)
		form = NewUserForm(request.POST)
		print(form.errors.as_data())
		if form.is_valid():
			user = form.save(commit=False)
			user.email = user.email.lower()

			user.save()
			#login(request, user)
			messages.success(request, "Registration successful." )
			send_activation_email(user,request)
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	
	return render (request=request, template_name="Structure/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			username = username.lower()
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if not user.is_email_verified:
				messages.error(request,"Email is not verified, please check inbox")
			elif user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	
	return render(request=request, template_name="Structure/login.html", context={"login_form":form,"request":request})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")

def my_life(request):
	#priorities = Priority.objects.get(pk=user_id)

	if request.user.is_authenticated:
			financial_entities = Financial_Entity.objects.filter(user=request.user)
			total = 0
			for entity in financial_entities:
				finaspects = Entity_Aspect.objects.filter(financial_entity=entity)
				for finaspect in finaspects:
					update = Entity_Amount.objects.filter(entity_aspect=finaspect).order_by('-date')
					try:
						total += update[0].amount
					except:
						pass


			total = round(total, 2)
			priorities = Priority.objects.filter(user=request.user)
			events = Event.objects.filter(user=request.user).order_by('-date')
			return render(request=request, template_name="Structure/my_life.html", context={"request":request,"priorities":priorities,"financial_entities":financial_entities,'events':events, 'amount':total})
	else:
		return redirect("/")

def add_priority(request):
	if request.POST:
		form = PriorityUploadForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
		return redirect('/life')
	return render(request, 'Structure/add_priority.html', context={'form':PriorityUploadForm})

def add_element(request, priority_id):
	if request.POST:
		form = ElementUploadForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.priority = Priority.objects.get(id=priority_id)
			obj.save()
		return redirect('/life/priority/'+str(priority_id))
	return render(request, 'Structure/add_element.html', context={'form':ElementUploadForm, 'priority_id':priority_id})

def add_aspect(request, priority_id, element_id):
	if request.POST:
		form = AspectUploadForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.element = Element.objects.get(id=element_id)
			obj.save()
		return redirect('/life/element/'+str(priority_id)+'/'+str(element_id))
	return render(request, 'Structure/add_aspect.html', context={'form':AspectUploadForm,'element_id':element_id,'priority_id':priority_id})

def priority(request, priority_id):
	if request.user.pk == Priority.objects.get(id = priority_id).user.pk:
		priority = Priority.objects.get(id=priority_id)
		elements = Element.objects.filter(priority=priority)
		return render(request=request, template_name="Structure/priority.html",context={"priority":priority,"elements":elements})
	else:
		raise Http404("Not yours!")

def element(request,priority_id,element_id):
	if request.user.pk == Element.objects.get(id = element_id).priority.user.pk:
		element = Element.objects.get(id=element_id)
		aspects = Aspect.objects.filter(element=element)
		return render(request=request, template_name="Structure/element.html",context={"element":element,"aspects":aspects,"priority_id":priority_id})
	else:
		raise Http404("Not yours!")
	
def aspect(request,priority_id, element_id, aspect_id):
	if request.user.pk == Aspect.objects.get(id = aspect_id).element.priority.user.pk:
		aspect = Aspect.objects.get(id=aspect_id)
		return render(request=request, template_name="Structure/aspect.html",context={"aspect":aspect,"element_id":element_id,"priority_id":priority_id})
	else:
		raise Http404("Not yours!")

def delete_priority(request,priority_id,delete):
	
	if delete==1:
		Priority.objects.get(pk=priority_id).delete()
		return redirect('/life')
	elif delete == 0:
		return render(request, template_name = "Structure/delete_priority.html",context={"priority_id":priority_id})
	elif delete==3 and request.user.pk == Priority.objects.get(id = priority_id).user.pk:
		priority = Priority.objects.get(id=priority_id)
		elements = Element.objects.filter(priority=priority)
		return render(request=request, template_name="Structure/priority.html",context={"priority":priority,"elements":elements})


def delete_element(request,priority_id,element_id,delete):
	if delete==1:
		Element.objects.get(pk=element_id).delete()
		return redirect('/life/priority/'+str(priority_id))
	elif delete == 0:
		return render(request, template_name = "Structure/delete_element.html",context={"priority_id":priority_id,"element_id":element_id})
	elif delete==3 and request.user.pk == Element.objects.get(id = element_id).priority.user.pk:
		element = Element.objects.get(id=element_id)
		aspects = Aspect.objects.filter(element=element)
		return render(request=request, template_name="Structure/element.html",context={"element":element,"aspects":aspects,"priority_id":priority_id})

def delete_aspect(request,priority_id,element_id,aspect_id,delete):
	if delete==1:#confirm
		Aspect.objects.get(pk=aspect_id).delete()
		return redirect('/life/element/'+str(priority_id)+'/'+str(element_id))
	elif delete == 0:#click delete in bar
		return render(request, template_name = "Structure/delete_aspect.html",context={"priority_id":priority_id,"element_id":element_id,"aspect_id":aspect_id})
	elif delete==3 and request.user.pk == Aspect.objects.get(id = aspect_id).element.priority.user.pk:#cancel
		aspect = Aspect.objects.get(id=aspect_id)
		return render(request=request, template_name="Structure/aspect.html",context={"aspect":aspect,"element_id":element_id,"priority_id":priority_id})

def edit_aspect(request, aspect_id, element_id, priority_id):
	aspect = Aspect.objects.get(id=aspect_id)

	if request.method == 'POST':
		form = AspectEditForm(request.POST, request.FILES, instance=aspect)
		if form.is_valid():
			if request.FILES:
				delete_file(aspect.image.path)
	# update the existing `Band` in the database

			form.save()
	# redirect to the detail page of the `Band` we just updated
		return redirect('/life/element/'+str(priority_id)+'/'+str(element_id))
	else:
		form = AspectEditForm(instance=aspect)

	return render(request,
	'Structure/edit_aspect.html',
	{'form':form,'element_id':element_id,'priority_id':priority_id,'aspect':aspect})

def edit_element(request, element_id, priority_id):
	element = Element.objects.get(id=element_id)

	if request.method == 'POST':
		form = ElementUploadForm(request.POST, request.FILES, instance=element)
		if form.is_valid():

	# update the existing `Band` in the database
			if request.FILES:
				delete_file(element.image.path)
			form.save()
	# redirect to the detail page of the `Band` we just updated
			return redirect('/life/priority/'+str(priority_id))
	else:
		form = ElementUploadForm(instance=element)

	return render(request,
	'Structure/edit_element.html',
	{'form': form,'priority_id': priority_id,'element':element})

def edit_priority(request, priority_id):
	priority = Priority.objects.get(id=priority_id)

	if request.method == 'POST':
		form = PriorityUploadForm(request.POST, request.FILES,instance=priority)
		if form.is_valid():
			if request.FILES:
				delete_file(priority.image.path)
			#image_path = priority.image.path
			#if os.path.exists(image_path):
			#	os.remove(image_path)
			#print('#####################')
			#obj = form.save(commit=False)

			#print(request.POST)

			#print('#####################')
			#obj.image = request.POST['image']
			#obj.save()
			form.save()
# redirect to the detail page of the `Band` we just updated
			return redirect('/life')
	else:
		form = PriorityUploadForm(instance=priority)

	return render(request,
'Structure/edit_priority.html',
{'form': form, 'priority':priority})

def activate_user(request, uidb64, token):
	try:
		uid=force_str(urlsafe_base64_decode(uidb64))
		user=User.objects.get(pk=uid)
	except Exception as e:
		user=None
		print(e)
	if user and generate_token.check_token(user,token):
		user.is_email_verified=True
		user.save()
		messages.add_message(request, messages.SUCCESS, 'Email verified, you can login')
		return redirect(reverse('login'))
	return render(request, 'Structure/authenticate/activate_failed.html',{'user':user})

def options(request):
	return render(request, 'Structure/options.html')

def email_reset(request, uidb64, token,email):
	try:
		uid=force_str(urlsafe_base64_decode(uidb64))
		user=User.objects.get(pk=uid)
	except Exception as e:
		user=None
		print(e)
	if user and generate_token.check_token(user,token):
		user.email=email
		user.save()
		messages.add_message(request, messages.SUCCESS, 'Email verified, you can login')
		return redirect(reverse('login'))
	return render(request, 'Structure/authenticate/activate.html',{'user':user})

def send_change_email(email_address, request):
	current_site = get_current_site(request)
	email_subject = 'Reset your email'
	
	email_body = render_to_string('Structure/reset/change_email.html',{'email':email_address,'user':request.user,'domain':current_site,'uid':urlsafe_base64_encode(force_bytes(request.user.pk)),'token':generate_token.make_token(request.user)})
	email = EmailMessage(subject=email_subject,body=email_body,from_email=settings.EMAIL_FROM_USER, to=[email_address])
	EmailThread(email).start()

def change_email(request):
	
	if request.method == "POST":
		print(request.POST)
		form = ChangeEmail(request.POST)
		print(form.errors.as_data())
		if form.is_valid():
			email = form.cleaned_data['email']
			email = email.lower()
			#login(request, user)
			messages.success(request, "Email change successful." )
			send_change_email(email,request)
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = ChangeEmail()
	return render (request=request, template_name="Structure/change_email.html", context={"form":form})

def entity(request, entity_id):
	if request.user.pk == Financial_Entity.objects.get(id = entity_id).user.pk:
		entity = Financial_Entity.objects.get(id=entity_id)
		finaspects = Entity_Aspect.objects.filter(financial_entity=entity)
		total=0
		for finaspect in finaspects:
			update = Entity_Amount.objects.filter(entity_aspect=finaspect).order_by('-date')
			try:
				total += update[0].amount
			except:
				pass
		total = round(total, 2)
		return render(request=request, template_name="Structure/financial-entity.html",context={"entity":entity,"finaspects":finaspects,'amount':total})
	else:
		raise Http404("Not yours!")



def finaspect(request,entity_id,finaspect_id):
	if request.user.pk == Entity_Aspect.objects.get(id = finaspect_id).financial_entity.user.pk:
		finaspect = Entity_Aspect.objects.get(pk=finaspect_id)
		updates = Entity_Amount.objects.filter(entity_aspect=finaspect)
		
		if updates:
			updates = updates.order_by('-date')
			growth = (float(updates[0].amount)-float(updates.reverse()[0].amount))/float(updates.reverse()[0].amount)*100
			first = updates[0]
		else:
			growth= 0
			first=None
		return render(request=request, template_name="Structure/finaspect.html",context={"finaspect":finaspect,"updates":updates,"entity_id":entity_id,"growth":growth,"first":first})
	else:
		raise Http404("Not yours!")

def update(request,entity_id, finaspect_id, update_id):
	if request.user.pk == Entity_Amount.objects.get(id = update_id).entity_aspect.financial_entity.user.pk:
		update = Entity_Amount.objects.get(id=update_id)
		return render(request=request, template_name="Structure/update.html",context={"update":update,"finaspect_id":finaspect_id,"entity_id":entity_id})
	else:
		raise Http404("Not yours!")

def edit_update(request, update_id, finaspect_id, entity_id):
	update = Entity_Amount.objects.get(id=update_id)

	if request.method == 'POST':
		form = UpdateUploadForm(request.POST, request.FILES, instance=update)
		if form.is_valid():
			
	# update the existing `Band` in the database

			form.save()
	# redirect to the detail page of the `Band` we just updated
		return redirect('/financial/'+str(entity_id)+'/'+str(finaspect_id)+'/'+str(update_id))
	else:
		form = UpdateUploadForm(instance=update)

	return render(request,
	'Structure/edit_entity_update.html',
	{'form':form,'finaspect_id':finaspect_id,'entity_id':entity_id,'update':update})

def edit_finaspect(request, finaspect_id, entity_id):
	finaspect = Entity_Aspect.objects.get(id=finaspect_id)

	if request.method == 'POST':
		form = FinAspectUploadForm(request.POST, request.FILES, instance=finaspect)
		if form.is_valid():

	# update the existing `Band` in the database
			if request.FILES:
				delete_file(finaspect.image.path)
			form.save()
	# redirect to the detail page of the `Band` we just updated
			return redirect('/financial/'+str(entity_id)+'/'+str(finaspect_id))
	else:
		form = FinAspectUploadForm(instance=finaspect)

	return render(request,
	'Structure/edit_finaspect.html',
	{'form': form,'entity_id': entity_id,'finaspect':finaspect})

def edit_entity(request, entity_id):
	entity = Financial_Entity.objects.get(id=entity_id)

	if request.method == 'POST':
		form = EntityUploadForm(request.POST, request.FILES,instance=entity)
		if form.is_valid():
			if request.FILES:
				delete_file(entity.image.path)

			form.save()

			return redirect('/financial/'+str(entity_id))
	else:
		form = EntityUploadForm(instance=entity)

	return render(request,
'Structure/edit_financial_entity.html',
{'form': form, 'entity':entity})

def delete_entity(request,entity_id,delete):
	
	if delete==1:
		Financial_Entity.objects.get(pk=entity_id).delete()
		return redirect('/life')
	elif delete == 0:
		return render(request, template_name = "Structure/delete_entity.html",context={"entity_id":entity_id})
	elif delete==3 and request.user.pk == Financial_Entity.objects.get(id = entity_id).user.pk:
		entity = Financial_Entity.objects.get(id=entity_id)
		finaspects = Entity_Aspect.objects.filter(financial_entity=entity)
		return render(request=request, template_name="Structure/financial-entity.html",context={"entity":entity,"finaspects":finaspects})


def delete_finaspect(request,entity_id,finaspect_id,delete):
	if delete==1:
		Entity_Aspect.objects.get(pk=finaspect_id).delete()
		return redirect('/financial/'+str(entity_id))
	elif delete == 0:
		return render(request, template_name = "Structure/delete_finaspect.html",context={"entity_id":entity_id,"finaspect_id":finaspect_id})
	elif delete==3 and request.user.pk == Entity_Aspect.objects.get(id = finaspect_id).financial_entity.user.pk:
		finaspect = Entity_Aspect.objects.get(id=finaspect_id)
		updates = Entity_Amount.objects.filter(entity_aspect=finaspect)
		return render(request=request, template_name="Structure/finaspect.html",context={"finaspect":finaspect,"updates":updates,"entity_id":entity_id})

def delete_update(request,entity_id,finaspect_id,update_id,delete):
	if delete==1:#confirm
		Entity_Amount.objects.get(pk=update_id).delete()
		return redirect('/financial/'+str(entity_id)+'/'+str(finaspect_id))
	elif delete == 0:#click delete in bar
		return render(request, template_name = "Structure/delete_update.html",context={"entity_id":entity_id,"finaspect_id":finaspect_id,"update_id":update_id})
	elif delete==3 and request.user.pk == Entity_Amount.objects.get(id = update_id).entity_aspect.financial_entity.user.pk:#cancel
		update = Entity_Amount.objects.get(id=update_id)
		return render(request=request, template_name="Structure/update.html",context={"update":update,"finaspect_id":finaspect_id,"entity_id":entity_id})

def add_entity(request):
	if request.POST:
		form = EntityUploadForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
		return redirect('/life')
	return render(request, 'Structure/add_entity.html', context={'form':EntityUploadForm})

def add_finaspect(request, entity_id):
	if request.POST:
		form = FinAspectUploadForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.financial_entity = Financial_Entity.objects.get(id=entity_id)
			obj.save()
		return redirect('/financial/'+str(entity_id))
	return render(request, 'Structure/add_finaspect.html', context={'form':FinAspectUploadForm, 'entity_id':entity_id})

def add_update(request, entity_id, finaspect_id):
	if request.POST:
		form = UpdateUploadForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.entity_aspect = Entity_Aspect.objects.get(pk=finaspect_id)
			obj.save()
		return redirect('/financial/'+str(entity_id)+'/'+str(finaspect_id))
	return render(request, 'Structure/add_financial_update.html', context={'form':UpdateUploadForm,'finaspect_id':finaspect_id,'entity_id':entity_id})

def add_event(request):
	if request.POST:
		form = EventUploadForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
		return redirect('/life')
	return render(request, 'Structure/add_event.html', context={'form':EventUploadForm})

def edit_event(request, event_id):
	event = Event.objects.get(id=event_id)

	if request.method == 'POST':
		form = EventUploadForm(request.POST, instance=event)
		if form.is_valid():
			if request.FILES:
				delete_file(event.image.path)

			form.save()

			return redirect('/event/'+str(event_id))
	else:
		form = EventUploadForm(instance=event)

	return render(request,
'Structure/edit_event.html',
{'form': form, 'event':event})

def delete_event(request,event_id,delete):
	
	if delete==1:
		Event.objects.get(pk=event_id).delete()
		return redirect('/life')
	elif delete == 0:
		return render(request, template_name = "Structure/delete_event.html",context={"event_id":event_id})
	elif delete==3 and request.user.pk == Event.objects.get(id = event_id).user.pk:
		event = Event.objects.get(id=event_id)
		return render(request=request, template_name="Structure/event.html",context={"event":event})

def event(request, event_id):
	if request.user.pk == Event.objects.get(id = event_id).user.pk:
		event = Event.objects.get(id=event_id)
		return render(request=request, template_name="Structure/event.html",context={"event":event})
	else:
		raise Http404("Not yours!")