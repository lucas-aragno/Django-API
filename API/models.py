from django.db import models
from datetime import datetime

class Session(models.Model):
	session_id = models.CharField(max_length=200)

	def __str__(self):
		return self.session_id


class Bar(models.Model):
    name = models.CharField(max_length = 100)

    def to_json(self):
      return {'name': self.name}

class List(models.Model):
	name = models.CharField(max_length=200)

	def to_json(self):
		json = []
		for user in self.user_set.all():
			json.append(user.to_json())
		return {'id' : self.id, 'list_name' : self.name, 'list' : json}

class User(models.Model):
	name = models.CharField(max_length=200)
	fb_uid = models.CharField(max_length=50)
	fb_token = models.CharField(max_length=100)
	session = models.OneToOneField(Session,null=True)
	list_place = models.ForeignKey(List,null = True)
	role = models.CharField(max_length=10,null=True)
        bares = models.ManyToManyField(Bar,null=True)

	def __str__(self):
		return self.name

	def has_session(self):
			return True if (self.session) else False

        def is_rpp(self):
	  return True if (self.role == "rpp") else False

	def is_bar(self):
	  return True if (self.role == "bar") else False

	def is_doorman(self):
          return True if(self.role == "doorman") else False

	def is_guest(self):
	  return True if (self.role == "guest") else False

	def is_from_facebook(self):
	  return True if (self.fb_token) else False

        def to_json(self):
	  json = []
	  for bar in self.bares.all():
	    json.append(bar.to_json())
	  return {'id' : self.id, 'name' : str(self.name), 'fb_token' : self.fb_token, 'fb_uid' : self.fb_uid, 'bar_list' : json}


class UserList(models.Model):
	user = models.ForeignKey(User)
	collection = models.ForeignKey(List)

class Item(models.Model):
  bar = models.ForeignKey(Bar)
  item_type = models.CharField(max_length=100)
  flyer = models.CharField(max_length=100,null=True)
  stock = models.IntegerField(default = 0)
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=400, null=True)

  def is_drink(self):
    return True if (self.item_type == "drink") else False

  def is_pass(self):
    return True if (self.item_type == "pass") else False

  def is_promo(self):
    return True if (self.item_type == "promo") else False

  def reduce_stock(self, amount):
  	self.stock = self.stock - amount
  	self.save()

  def increase_amount(self, amount):
  	self.stock = self.stock + amount
  	self.save()

  
class Ticket(models.Model):
  used_at = models.DateTimeField(null=True)
  owner = models.ForeignKey('User')
  item = models.ForeignKey('Item', null=True)
  
  

  def use(self):
    self.used_at = datetime.now()
    self.save()

  def ticket_type(self):
    return str(self.item.item_type)

  def is_used(self):
    return True if (self.used_at) else False

  def to_json(self):
    return {'flyer' : str(self.item.flyer), 'name' : str(self.item.name), 'used_at' : str(self.used_at) }


