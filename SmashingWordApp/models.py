from django.db import models
import django
from django.http import Http404

# Create your models here.
SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4
FAILURE = -5

class User(models.Model):
	userName = models.TextField(max_length=128, primary_key=True, blank=False)
	balance=models.IntegerField()
	mpScore = models.IntegerField()
	spScore = models.IntegerField()


	
	def __unicode__(self):
		return str((self.userName, self.balance, self.mpScore, self.spScore))

	def TESTAPI_resetFixture(self):
		User.objects.all().delete()
		return SUCCESS
	def updateBalance(self, inUserName, inBalance):
		if inBalance<0:
			return (FAILURE,{})
		try:	
			temp = self.userExist(inUserName)
			if (temp[0]==False):
				self.add(inUserName, Balance = inBalance)
			else:
				dbResult = User.objects.get(userName = inUserName)
				dbResult.balance = inBalance
				dbResult.save()
			#print "success"
			code = SUCCESS
		except Exception as e:
			print e
			print "faile"
			code=FAILURE
		return (code, {})
	
	def add(self,inUserName, Balance=0, MpScore=0, SpScore=0):
		code=1
		print SpScore
		if self.userExist(inUserName)[0]:
			code=ERR_USER_EXISTS
		if not self.validateUsername(inUserName):
			code = ERR_BAD_USERNAME
		tobeAdd = User(userName=inUserName, balance=Balance, mpScore=MpScore, spScore = SpScore)
		tobeAdd.save()
		return (code,{})
	def getUserInfo(self, inUser = None):
		try:	
			if inUser!=None:
				dbResult = User.objects.get(userName = inUser)
			else:	
				dbResult = User.objects.all()
			return (SUCCESS, self.parseHandler(dbResult, 'fullInfo'))
		except Exception as e:
			print "fuck you!!!!"
			print e
			return (FAILURE,{})
			

	def Top10Single(self):
		try:
			print "query top10"
			dbResult = User.objects.order_by("-spScore")[0:10]
			print(type(dbResult))
			return (SUCCESS, self.parseHandler(dbResult,'easy', True))
		except Exception as e:
			print (e)
			return (FAILURE, {})
	def Top10Multiple(self):
		try:
			print "query multiple top 10"
			dbResult = User.objects.order_by("-mpScore")[0:10]
			return (SUCCESS, self.parseHandler(dbResult,'easy', False))
		except Exception as e:
			print (e)
			return (FAILURE, {})

	def saveScoressSingle(self,inUserName, inScore):
		try:	
			temp = self.userExist(inUserName)
			if (temp[0]==False):
				self.add(inUserName, SpScore=inScore)
				print "add user"
			else:
				dbResult = User.objects.get(userName = inUserName)
				if inScore > dbResult.spScore:
					dbResult.spScore = inScore
				dbResult.save()
			#print "success"
			code = SUCCESS
		except Exception as e:
			print e
			print "faile"
			code=FAILURE
		return (code, {})

	def saveScoresMultiple(self,inUserName, inScore):
		try:
			temp = self.userExist(inUserName)
			if (temp[0]==False):
				self.add(inUserName, MpScore=inScore)
			else:
				dbResult = User.objects.get(userName = inUserName)
				if inScore > dbResult.mpScore:
					dbResult.mpScore = inScore
				dbResult.save()
			#print "success"
			code = SUCCESS
		except:
			code=FAILURE
		return (code, {})
			
	def userExist(self,inUserName):
		try:
			dbresult = User.objects.get(userName = inUserName)
			Exist = True
		except:
			Exist=False
			dbresult = None
		return (Exist,dbresult)

	def validateUsername(self, name):
		return name!="" and len(name)<=	128

	def parseHandler(self,userObj, mode = 'fullInfo', singleOrNot = True):
		if userObj==[] or userObj==None:
			return {}
		if type(userObj)==django.db.models.query.QuerySet:
			data=[]
			for elem in userObj:
				if mode=='fullInfo':
					data.append(self.parser(elem))
				else:
					if singleOrNot:
						data.append(self.easyParserSingle(elem))
					else:
						data.append(self.easyParserMultiple(elem))
			return data
		else:
			if mode == 'fullInfo':
				return self.parser(userObj)
			else:
				if singleOrNot:
					return self.easyParserSingle(userObj)
				else:
					return self.easyParserMultiple(userObj)
	def parser(self, user):
		return {'user':user.userName, 'balance':user.balance,'mpScore':user.mpScore, 'spScore':user.spScore}
	def easyParserSingle(self, user):
		return {'user':user.userName, 'score':user.spScore}
	def easyParserMultiple(self, user):
		return {'user':user.userName, 'score':user.mpScore}


class Item(models.Model):
	name = models.TextField(max_length=128, blank=False)
	price = models.IntegerField(blank=False)
	
	def getItemInfo(self,ItemName):
		try:
			dbResult = Item.objects.get(name = ItemName)
			print
			return (SUCCESS, self.ItemParser(dbResult))
		except Exception as e:
			return (FAILURE,{})

	def ItemParser(self, item):
		return {'ItemName':item.name, 'price': item.price}

	def updateItem(self, Name, Price):
		try:
			temp= self.ItemExist(Name)
			if temp[0]:
				print "update price"
				print Price
				temp[1].price = Price
				temp[1].save()
			else:
				tobeAdd = Item(name=Name, price= Price)
				tobeAdd.save()
			return (SUCCESS,{})
		except Exception as e:
			print e
			return (FAILURE,{})


	def ItemExist(self,inItemName):
		try:
			dbresult = Item.objects.get(name = inItemName)
			Exist = True
		except:
			Exist=False
			dbresult = None
		return (Exist,dbresult)
		


class OwnItem(models.Model):
	userName = models.ForeignKey(User)
	name = models.ForeignKey(Item)

	def addPair(self,user, ItemName):
		try:
			tobeAdd = addPair(user,ItemName)
			tobeAdd.save()
		except Exception as e:
			print e
			return (FAILURE,{})

	def deletePair(self, user,ItemName):
		try:
			temp = OwnItem.objects.get(userName = user, name = ItemName)
			if type(temp) == django.db.models.query.QuerySet:
				for elem in temp:
					elem.delete()
					break
			else:
				temp.delete()
			return (SUCCESS,{})
		except Exception as e:
			print e
			return (FAILURE,{})
	






