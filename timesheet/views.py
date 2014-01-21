from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Main user auth
from django.contrib.auth.models import User
# forms
from timesheet.forms import EntryForm
# models
from users.models import UserProfile
from timesheet.models import Time
# json ajax
from django.utils import simplejson

# Create your views here.
def index(request):
	# init all entries
	all_entries = ''

	if request.user.is_authenticated() and request.user.is_active:
		# get entries made by the user
		all_entries = Time.objects.filter(user=request.user)
		# will use datatables to render entries
	return render(request,'timesheet/index.html', {'entries':all_entries})

def index_json(request):
	if request.user.is_authenticated() and request.user.is_active:
		# pull entries only for current user
		all_entries = Time.objects.filter(user=request.user)
		# compile entries into a list
		data = []
		for entry in all_entries:
			entry_data = []
			entry_data.append(str(entry.date))
			entry_data.append(str(entry.title))
			entry_data.append(str(entry.hours))
			entry_data.append(str(entry.comments))
			entry_data.append(str(entry.pk))
			data.append(entry_data)

		# # for datatables
		# json_data = {'aaData': data}
		# for other
		json_data = {request.user.username: data}

		json = simplejson.dumps(json_data)

		if json:
			return HttpResponse(json, mimetype='application/json')
		else:
			return HttpResponse('')
	else:
		# access is not allowed
		raise Http404

def about(request):
	# TODO
	return render(request,'timesheet/about.html')


def entry(request,entry_url):
	# init vars
	entry_form = ''
	entry = ''
	entry_url_id = int(entry_url)
	wrong_user = False

	# if a correct number is used and the user is authenticated
	if entry_url_id and request.user.is_authenticated() and request.user.is_active:
		# get the entry based on primary key
		entry = Time.objects.get(pk=entry_url_id)

		# only the creator of the entry is allowed to edit (or admin)
		if entry.user != request.user:
			wrong_user = True

		elif request.method == 'POST':
			
			entry_form = EntryForm(data=request.POST)
			if entry_form.is_valid():
				# save but dont commit
				new_entry = entry_form.save(commit=False)
				# insert user as before
				new_entry.user = request.user
				# use old primary key
				new_entry.pk = entry_url_id
				# delete old entry - new entry overrides it
				entry.delete()

				if not request.POST.get('delete'):
					new_entry.save()
				# redirect to index

				return HttpResponseRedirect('/timesheet/') 
		else:
			# use current db data for form
			entry_form = EntryForm(instance=entry)


	return render(request,'timesheet/entry.html',{'entry_form':entry_form,'wrong_user':wrong_user,'entry':entry})



def newEntry(request):
	# init vars
	error = ''

	# only a valid user is allowed to create a new entry
	if request.user.is_authenticated() and request.user.is_active and request.method == 'POST':
		entry_form = EntryForm(data=request.POST)


		if entry_form.is_valid():
			entry = entry_form.save(commit=False)
			entry.user = request.user
			entry.save()
			return HttpResponseRedirect('/timesheet/')
		else:
			error = 'Invalid form'

	else:
		entry_form = EntryForm()

	return render(request,'timesheet/new.html',{'form':entry_form,'error':error})



# should populate db with some test data
# modify with any changes to models etc
def test_data(request):
	status_message = ''

	if request.user.is_authenticated:
		all_test_entries = []
		entry = Time(title='Test 1',date='2014-1-1',hours=1,user=request.user,comments='This is test entry 1')
		all_test_entries.append(entry)
		entry = Time(title='Test 2',date='2014-2-2',hours=2,user=request.user,comments='This is test entry 2')
		all_test_entries.append(entry)
		entry = Time(title='Test 3',date='2014-3-3',hours=3,user=request.user,comments='')
		all_test_entries.append(entry)
		entry = Time(title='Test 4',date='2014-4-4',hours=4,user=request.user,comments='<h1>This is test entry 4</h1>')
		all_test_entries.append(entry)
		entry = Time(title='Test 5',date='2014-5-5',hours=5,user=request.user,comments='This is test entry 5')
		all_test_entries.append(entry)
		entry = Time(title='Test 6',date='2014-6-6',hours=6,user=request.user,comments='This is test entry 6')
		all_test_entries.append(entry)

		try:
			for e in all_test_entries:
				e.save()
			status_message = 'Test data insert successful'
		except Exception, e:
			status_message = 'Test data insert unsuccessful'
		
			
		
	else:
		status_message = 'You are not authorized to insert test data.  Please login'


	return HttpResponse(status_message+' <br> <a href="/">Index</a>')
