# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from SmashingWordApp.models import User
from SmashingWordApp.models import Item
from SmashingWordApp.models import OwnItem
# import the logging library
from django.views.decorators.csrf import csrf_protect
import logging
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import sys 
from os import curdir, sep
import os
from django.http import Http404
import json
import models
import cgi
import tempfile
import traceback
import StringIO
import unittest
from testAdditional import TestAmbition
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
g_user = models.User()
g_item = models.Item()
g_OwnItem = models.OwnItem()


SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4
FAILURE=-5



# Any result from models.pya is a tuple of two, where first item is the code, second item is the data. Data can be either array or dictionary. When it's an array, that means it contains an array of user info. when it's a dictionary, that means it only contains info of one user.	


# Get an instance of a logger
log = logging.getLogger(__name__)
@csrf_exempt
def index(request): 
	if request.method == "POST":
		if (request.path.find("/users/SaveScores/")==0 )or (request.path.find("/users/updateBalance")==0):
			return UserController(request)
		elif request.path.find("/TESTAPI/")==0:
			return TESTController(request)
		elif request.path.find("/items/post/") ==0:
			return ItemPostController(request)
		else:
			raise Http404
	elif request.method=="GET":
		content_type="application/json"
		if request.path.find("/diulama/items")==0:
			g_item.insertObjects()
		elif request.path.find("/users/Top10Scores")==0:
			return TopScoresController(request)
		elif request.path.find("/items/view")==0:
			return ItemGetConroller(request)
		elif request.path.find("/users/getUserInfo")==0:
			inData = json.loads(request.body)
			if 'user' in inData:
				inUserName = inData["user"]
				result = g_user.getUserInfo(inUserName)
			else:
				result = g_user.getUserInfo()
			return HttpResponse(json.dumps({'Code': result[0], 'data':result[1]}),content_type="application/json" )
		else:
			return render_to_response('SmashingWordApp'+request.path,mimetype="text/html")


@csrf_exempt
def ItemGetConroller(request):
	inData=json.loads(request.body)
	if 'ItemName' in inData:
		ItemName = inData['ItemName']
	 	result=g_item.getItemInfo(ItemName)
		return HttpResponse(json.dumps({'Code': result[0], 'data':result[1]}),content_type="application/json" )
	else:
		
		return HttpResponse(json.dumps({'Code': FAILURE, 'data':'Missing Item Name'}),content_type="application/json" )



@csrf_exempt
def ItemPostController(request):
	inData = json.loads(request.body)
	if 'ItemName' in inData:
		ItemName = inData['ItemName']
	if 'user' in inData:
		user = inData['user']
	if 'price' in inData:
		price = inData['price']
	if request.path == "/items/post/buy":
		print "1234"
		dbUser = g_user.getUserInfo(user)[1]
		dbItem = g_item.getItemInfo(ItemName)[1]
		print "12341212131"
		if (dbUser=={} or dbItem=={}):
			return HttpResponse(json.dumps({'Code': FAILURE, 'data':{}}),content_type="application/json" )
		else:
			itemPrice = dbItem['price']
			userBalance = dbUser['balance']
			if (userBalance - itemPrice>=0):
				finalBalance = userBalance - itemPrice
				g_user.updateBalance(user, finalBalance)
				result = g_OwnItem.addPair(user, ItemName)
			else:
				print "1234!!!!"
				return HttpResponse(json.dumps({'Code': FAILURE, 'data':{}}),content_type="application/json" )
	elif request.path  == "/items/post/use":
		result = g_OwnItem.deletePair(user,ItemName)
	elif request.path == "/items/post/update":
		result = g_item.updateItem(ItemName,price)
	else:
		raise Http404
	return HttpResponse(json.dumps({'Code': result[0], 'data':result[1]}),content_type="application/json" )



@csrf_exempt
def TESTController(request):
	if request.path=="/TESTAPI/resetFixture":
		g_user.TESTAPI_resetFixture()
		return HttpResponse(json.dumps({'Code': SUCCESS}),content_type="application/json" )
	elif request.path== "/TESTAPI/unitTests":
		buf = StringIO.StringIO()
		suite = unittest.TESTLoader().loadTestsFromTestCase(TestAmibition)
		result = unittest.TextTestRunner(stream = buf, verbosity=2).run(suite)
		return HttpResponse(json.dumps({'totalTests': result.testsRun ,  'nrFailed': len(result.failures), 'output':buf.getvalue()}),content_type="application/json" )
            
        else:
            raise Http404
@csrf_exempt
def TopScoresController(request): 
	if request.path =="/users/Top10Scores/single":
		result = g_user.Top10Single()
	elif request.path =="/users/Top10Scores/multiple":
		result = g_user.Top10Multiple()
	else:
		raise Http404
	return HttpResponse(json.dumps({'Code': result[0], 'data':result[1]}),content_type="application/json" )

@csrf_exempt
def InfoController(request):
	if 'user' in inData:
		inUserName = inData["user"]
		print "3333"
		result = g_user.getUserInfo(inUserName)
	else:
		result = g_user.getUserInfo()
	return HttpResponse(json.dumps({'Code': result[0], 'data':result[1]}),content_type="application/json" )

@csrf_exempt
def UserController(request):
	inData = json.loads(request.body)
	if 'user' in inData:
		inUserName = inData["user"]
	if 'score' in inData:
		inScore = inData['score']
	if 'balance' in inData:
		inBalance = inData['balance']

	if request.path =="/users/SaveScores/single":
		result = g_user.saveScoressSingle(inUserName, inScore)

	elif request.path =="/users/SaveScores/multiple":
		result = g_user.saveScoresMultiple(inUserName, inScore)

	elif request.path == "/users/updateBalance":
		result = g_user.updateBalance(inUserName, inBalance)

	else:
		raise Http404
	return HttpResponse(json.dumps({'Code': result[0], 'data':result[1]}),content_type="application/json" )

		
