  
import uuid
import simplejson as json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from API.models import *

# Helpers

def json_response(message):
  return {'message' : message}

def current_user(session_id):
  try:
    user = User.objects.all().filter(session = Session.objects.all().filter(session_id = session_id)).get()
  except User.DoesNotExist:
    user = None


#End of Helpers


# Decorators

def session_id_required(f):

  def wrapper(*args, **kw):
    if (args[0].POST != {}):
      session_id = args[0].POST.get('session_id',False)
    else:
      session_id = str(args[0].GET.get('session_id',False))
    try:
      session = Session.objects.all().filter(session_id = session_id).get()
    except Session.DoesNotExist:
      session = None
    if session:
      return f(*args, **kw)
    else:
      return HttpResponse(json.dumps(json_response('invalid session_token')))
  return wrapper

# End of decorators


# SESSIONS
@session_id_required
def logout(request):
  session_id = request.POST.get('session_id',False)
  try:
    session = Session.objects.all().filter(session_id = session_id).get()
  except Session.DoesNotExist:
    session = None
  if session:
    session.delete()
    return HttpResponse(json.dumps(json_response('ok')))
  else:
    return HttpResponse(json.dumps(json_response('error')))

def login(request):
  fb_uid = request.POST.get('fb_uid',False)
  fb_name = request.POST.get('fb_name',False)
  try:
    user = User.objects.all().filter(fb_uid = fb_uid).get()
  except User.DoesNotExist:
    user = None
  if user and not user.has_session():
    new_session = Session(session_id = str(uuid.uuid4()))
    new_session.save()
    user.session = new_session
    user.save()
    response = dict({'message' : 'ok', 'session_id' : new_session.session_id }.items() + user.to_json().items())
    return HttpResponse(json.dumps(response), content_type = 'application/javascript; charset=utf8')
  elif user and user.has_session():
  	response = dict({'message': 'ok', 'name' : user.name, 'session_id' : user.session.session_id}.items() + user.to_json().items())
        return HttpResponse(json.dumps(response))
  else:
  	user = User(name = fb_name, session = Session(session_id = str(uuid.uuid4())), fb_uid = fb_uid)
  	user.save()
  	response = dict({'message': 'ok', 'name' : user.name, 'session_id' : user.session.session_id}.items() + user.to_json().items())
  	return HttpResponse(json.dumps(response))


# END OF SESSIONS

#USERS

@session_id_required
def get_user_by_id(request):
  user_id = request.GET.get('user_id',False)
  try:
    user = User.objects.all().filter(id = user_id).get()
  except User.DoesNotExist:
    user = None
  if user:
    response = user.to_json()
  else:
    response = json_response('error')
  return HttpResponse(json.dumps(response))

@session_id_required
def create_list_by_user_id(request):
  user_id = request.POST.get('user_id',False)
  list_name = request.POST.get('list_name',False)
  try:
    user = User.objects.all().filter(id = user_id).get()
  except User.DoesNotExist:
    user = None
  if user:
    new_list = List(name = list_name)
    new_list.save()
    join = UserList(user = user, collection = new_list)
    join.save()
    return HttpResponse(json.dumps(new_list.to_json()))
  else:
   response = HttpResponse(json.dumps(json_response('error')))

@session_id_required
def delete_list_by_user_id(request):
  user_id = request.POST.get('user_id',False)
  list_name = request.POST.get('list_name',False)
  try:
    user = User.objects.all().filter(id = user_id).get()
  except User.DoesNotExist:
    user = None
  if user:
    new_list = List(name = list_name)
    new_list.save()
    join = UserList(user = user, collection = new_list)
    join.delete()
    return HttpResponse(json.dumps(json_response('ok')))
  else:
   response = HttpResponse(json.dumps(json_response('error')))


@session_id_required
def get_user_lists(request):
  user_id = request.GET.get('user_id',False)
  try:
    user = User.objects.all().filter(id = user_id).get()
  except User.DoesNotExist:
    user = None
  if user:
    response = []
    lists = UserList.objects.filter(user = user)
    for l in lists:
      response.append(l.collection.to_json())
    return HttpResponse(json.dumps(response))
  else:
    return HttpResponse(json.dumps(json_response('error')))

@session_id_required
def add_user_to_list(request):
  list_id = request.POST.get('list_id', False)
  user_id = request.POST.get('user_id', False)
  try:
    l = List.objects.get(id = list_id)
    user = User.objects.get(id = user_id)
  except List.DoesNotExists:
    l = None
  except User.DoesNotExists:
    user = None
  if l and user:
    ul = UserList.objects.get(collection = l)
    ul.collection.user_set.add(user)
    ul.collection.save()
    return HttpResponse(json.dumps(ul.collection.to_json()))
  else:
    return HttpResponse(json.dumps(json_response('error')))

@session_id_required
def remove_user_from_list(request):
  list_id = request.POST.get('list_id', False)
  user_id = request.POST.get('user_id', False)
  try:
    l = List.objects.get(id = list_id)
    user = User.objects.get(id = user_id)
  except List.DoesNotExists:
    l = None
  except User.DoesNotExists:
    user = None
  if l and user:
    ul = UserList.objects.get(collection = l)
    ul.collection.user_set.remove(user)
    ul.collection.save()
    return HttpResponse(json.dumps(ul.collection.to_json()))
  else:
    return HttpResponse(json.dumps(json_response('error')))

# END OF USERS


# Passes

@session_id_required
def get_ticket_by_user_id_and_bar_id(resuqest):
  owner = User.objects.all().filter(id = request.GET.get('user_id',False))
  bar = Bar.objects.all().filter(id = request.GET.get('bar_id',False))
  tickets = Tickets.objects.all().filter(owner = owner, bar = bar)
  response = []
  for ticket in tickets:
    if (ticket.pass_type == request.GET.get('ticket_type',False)):
      response.append(ticket.to_json())
  return HttpResponse(json.dumps(response))


def index(request):

	users = User.objects.all()
        #response = serializers.serialize('json', users)
	return JsonResponse(model_to_dict(users))
