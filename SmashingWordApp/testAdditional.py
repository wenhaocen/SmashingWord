"""
Each file that starts with test... in this directory is scanned for subclasses of unittest.TestCase or testLib.RestTestCase
"""

import unittest
import os
import testLib

        
class TestAmbition(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = None, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)
	
    #This method is to simlify the input dict, return a dict only contains spScore and mpScore and user. 
    def extractDict(self, inputDict):
	try:
		temp = dict()
		temp['Code'] = inputDict['Code']
		temp['data'] = dict()
		if 'user' in inputDict['data']:
			temp['data']['user'] = inputDict['data']['user']
		if 'spScore' in inputDict['data']:
			temp['data']['spScore'] = inputDict['data']['spScore']
		if 'mpScore' in inputDict['data']:
			temp['data']['mpScore'] = inputDict['data']['mpScore']
		return temp
	except Exception as e:	
		print e
   
    #check if we can update user balance correctly
    def testupdateBalance(self):
	self.makeRequest("/users/updateBalance", method="POST", data={'user':'1', 'balance':1})
	self.makeRequest("/users/updateBalance", method="POST", data={'user':'1', 'balance':2})
	responseData = self.makeRequest("/users/getUserInfo", method="GET", data={'user':'1'})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS, 'data':{'user':'1', 'mpScore':0, 'spScore':0,'balance':2}},responseData)
	

    #check if a single player score is saved correctly
    def testSaveSingleScore(self):
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'1', 'score':1})
	responseData = self.makeRequest("/users/getUserInfo", method="GET", data={'user':'1'})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS, 'data':{'user':'1', 'mpScore':0, 'spScore':1}}, self.extractDict(responseData))

    #check if a multiple player score is saved correctly
    def testSaveSingleScore(self):
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':1})
	responseData = self.makeRequest("/users/getUserInfo", method="GET", data={'user':'1'})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS, 'data':{'user':'1', 'mpScore':1, 'spScore':0}}, self.extractDict(responseData))

    #check if single score and multiple user score are saved into correct field in db
    def testSaveCorrect(self):
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'1', 'score':1})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':2})
	responseData = self.makeRequest("/users/getUserInfo", method="GET", data={'user':'1'})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS,'data':{'user':'1', 'spScore':0, 'mpScore':2,'balance':0}}, responseData )
  

    #Test the same thing as above except the following is multiple play score version.
    def testOverwriteMultipleScore(self):
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':1})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':12})
	responseData = self.makeRequest("/users/getUserInfo", method="GET", data={'user':'1'})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS, 'data': {'user':'1', 'spScore':0, 'mpScore':12}}, self.extractDict(responseData) )

    #Test the over write actions to single player score and multiple player score don't inference each other
    def testOverWriteCross(self):
    	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':2})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':12})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'1', 'score':1})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'1', 'score':13})
	responseData = self.makeRequest("/users/getUserInfo", method="GET", data={'user':'1'})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS, 'data': {'user':'1', 'spScore':0, 'mpScore':12}}, self.extractDict(responseData) )
	
    #Add 12 single user score, see if we can query the correct top 10 single user score;
    def testTop10Single(self):
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'1', 'score':1})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'2', 'score':2})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'3', 'score':3})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'4', 'score':4})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'5', 'score':5})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'6', 'score':6})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'7', 'score':7})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'8', 'score':8})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'9', 'score':9})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'10', 'score':10})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'11', 'score':11})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'12', 'score':12})
	respData = self.makeRequest("/users/Top10Scores/single", method="POST",data={})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS,'data':[12,11,10,9,8,7,6,5,4,3]},respData)

    #Due to my special implementation, we need to check whether backend return multiple copies of a score if we insert dulplicate again and again. 
    def testTop10SingleOverlap(self):
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'1', 'score':1})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'2', 'score':1})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'3', 'score':3})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'4', 'score':2})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'5', 'score':4})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'6', 'score':9})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'7', 'score':9})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'8', 'score':12})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'9', 'score':10})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'10', 'score':10})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'11', 'score':11})
	self.makeRequest("/users/SaveScores/single", method="POST", data={'user':'12', 'score':12})
	respData = self.makeRequest("/users/Top10Scores/single", method="POST",data={})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS,'data':[12,12,11,10,10,9,9,4,3,2]},respData)

    # Just test the regular query for top 10 multiplayer scores.
    def testTop10Multiple(self):
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':1})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'2', 'score':2})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'3', 'score':3})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'4', 'score':4})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'5', 'score':5})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'6', 'score':6})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'7', 'score':7})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'8', 'score':8})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'9', 'score':9})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'10', 'score':10})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'11', 'score':11})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'12', 'score':12})
	respData = self.makeRequest("/users/Top10Scores/multiple", method="POST",data={})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS,'data':[{'user':'12', 'score':12},{'user':'11', 'score':11},{'user':'10', 'score':10},{'user':'9', 'score':9},{'user':'8', 'score':8},{'user':'7', 'score':7},{'user':'6', 'score':6},{'user':'5', 'score':5},{'user':'4', 'score':4},{'user':'3', 'score':3}]},respData)


    #Test if results are correct if there're less than 10 players in db, while we try to query Top 10 scores.
    def testTop10withoutEnoughPlayer(self):
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':1})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'2', 'score':2})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'3', 'score':3})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'4', 'score':4})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'5', 'score':5})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'6', 'score':6})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'7', 'score':7})
	respData = self.makeRequest("/users/Top10Scores/multiple", method="POST",data={})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS,'data':[{'user':'7', 'score':7},{'user':'6', 'score':6},{'user':'5', 'score':5},{'user':'4', 'score':4},{'user':'3', 'score':3}, {'user':'2', 'score':2}, {'user':'1', 'score':1}]},respData)


    #Make sure querying top 10 single players score doens't return or affected by the top 10 multiplayer score; 
    def testTop10CrossSingle(self):
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':12})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'2', 'score':11})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'3', 'score':10})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'4', 'score':9})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'5', 'score':8})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'6', 'score':7})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'7', 'score':6})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'8', 'score':5})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'9', 'score':4})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'10', 'score':3})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'11', 'score':2})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'12', 'score':1})

	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':1})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':2})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':3})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':4})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':5})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':6})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':7})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':8})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':9})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':10})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':11})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':12})
	respData = self.makeRequest("/users/Top10Scores/single", method="POST",data={})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS,'data':[12,11,10,9,8,7,6,5,4,3]},respData)



    def testTop10Multiple(self):
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1', 'score':1})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'2', 'score':2})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'3', 'score':3})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'4', 'score':4})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'5', 'score':5})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'6', 'score':6})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'7', 'score':7})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'8', 'score':8})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'9', 'score':9})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'10', 'score':10})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'11', 'score':11})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'12', 'score':12})
	respData = self.makeRequest("/users/Top10Scores/multiple", method="POST",data={})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS,'data':[{'user':'12', 'score':12},{'user':'11', 'score':11},{'user':'10', 'score':10},{'user':'9', 'score':9},{'user':'8', 'score':8},{'user':'7', 'score':7},{'user':'6', 'score':6},{'user':'5', 'score':5},{'user':'4', 'score':4},{'user':'3', 'score':3}]},respData)

    #Make sure querying top 10 multiple players score doens't return or affected by the top 10 single score; 
    def testTop10CrossMultiple(self):
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'1','score':12})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'2','score':11})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'3','score':10})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'4','score':9})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'5','score':8})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'6','score':7})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'7','score':6})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'8','score':5})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'9','score':4})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'10','score':3})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'11','score':2})
	self.makeRequest("/users/SaveScores/multiple", method="POST", data={'user':'12','score':1})

	self.makeRequest("/users/SaveScores/single", method="POST", data={'score':1})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':2})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':3})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':4})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':5})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':6})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':7})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':8})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':9})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':10})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':11})
	self.makeRequest("/users/SaveScores/single", method="POST", data={ 'score':12})
	respData = self.makeRequest("/users/Top10Scores/multiple", method="POST",data={})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS,'data':[{'user':'1', 'score':12},{'user':'2', 'score':11},{'user':'3', 'score':10},{'user':'4', 'score':9},{'user':'5', 'score':8},{'user':'6', 'score':7},{'user':'7', 'score':6},{'user':'8', 'score':5},{'user':'9', 'score':4},{'user':'10', 'score':3}]},respData)


	#The following tests are for shop or items.

    #See if we can add item to database successfully
    def testAddItem(self):
	self.makeRequest("/items/post/update", method="POST", data={'ItemName':'testPowerUp', 'price':12})
	respData = self.makeRequest("/items/view", method="GET",data={'ItemName':'testPowerUp'})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS, 'data':{'ItemName':'testPowerUp','price':12}}, respData)
    #Test if we can update the price of an item correctly
    def testUpdataItem(self):
	self.makeRequest("/items/post/update", method="POST", data={'ItemName':'testPowerUp', 'price':12})
	self.makeRequest("/items/post/update", method="POST", data={'ItemName':'testPowerUp', 'price':13})
	respData = self.makeRequest("/items/view", method="GET",data={'ItemName':'testPowerUp'})
	self.assertDictEqual({'Code':testLib.RestTestCase.SUCCESS, 'data':{'ItemName':'testPowerUp','price':13}}, respData)

    #Make sure we block user who try to buy stuff without emough money
    def testBuyWithoutMoney(self):
	self.makeRequest("/items/post/update", method="POST", data={'ItemName':'testPowerUp', 'price':12})
        self.makeRequest("/users/updateBalance", method="POST", data={'user':'1', 'balance':2})
	respData = self.makeRequest("/items/post/buy", method="POST", data={'ItemName':'testPowerUp', 'user':'1'})
	self.assertDictEqual({'Code':-5, 'data':{}}, respData)

    #Test if an user can buy an item successfully if one has enough money
    def testBuySuccess(self):
	self.makeRequest("/items/post/update", method="POST", data={'ItemName':'testPowerUp', 'price':12})
	self.makeRequest("/users/updateBalance", method="POST", data={'user':'1', 'balance':17})
	respData = self.makeRequest("/items/post/buy", method="POST", data={'ItemName':'testPowerUp', 'user':'1'})
	self.assertDictEqual({'Code':1, 'data':{}}, respData)

    def testBuyAmountCorrect(self):
	self.makeRequest("/items/post/update", method="POST", data={'ItemName':'testPowerUp', 'price':12})
	self.makeRequest("/users/updateBalance", method="POST", data={'user':'1', 'balance':40})
	respData = self.makeRequest("/items/post/buy", method="POST", data={'ItemName':'testPowerUp', 'user':'1'})
	respData = self.makeRequest("/items/post/buy", method="POST", data={'ItemName':'testPowerUp', 'user':'1'})
	respData = self.makeRequest("/items/post/get", method="POST", data={'user':'1'})
	self.assertDictEqual(respData, {'Code':1,'data':[{'name':'testPowerUp', 'amount':2}]})




	



	
	
	




	
    



    
