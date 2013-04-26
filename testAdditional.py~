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
    #Long username. >128
    def testAdd2(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : '1'*200, 'password' : 'password'} )
        self.assertResponse(respData, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)
    #Emtpy username
    def testAdd3(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : '', 'password' : 'password'} )
        self.assertResponse(respData, errCode=testLib.RestTestCase.ERR_BAD_USERNAME)
    #Regular Add user, success
    def testAdd4(self):
	respData = self.makeRequest("/users/add", method="POST", data={'user':'wenhaocen','password':'password'})
	self.assertResponse(respData, count=1, errCode=testLib.RestTestCase.SUCCESS)
    #Try to add user that already exists
    def testAdd5(self):
	respData = self.makeRequest("/users/add", method="POST", data={'user':'wenhaocen', 'password': 'wenhaocen'})
	respData = self.makeRequest("/users/add", method="POST", data={'user':'wenhaocen', 'password': 'wenhaocen'})
	self.assertResponse(respData,errCode = testLib.RestTestCase.ERR_USER_EXISTS)
    #Add user with empty password, should return success
    def testAdd6(self):
	respData = self.makeRequest("/users/add", method="POST", data={'user':'wenhaocen', 'password': ''}) 
	self.assertResponse(respData, count=1, errCode=testLib.RestTestCase.SUCCESS) 
    #Try to login with user doesn't exist
    def testLogin(self):
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'wenhaocen', 'password' : 'wenhaocen'} )
        self.assertResponse(respData, count = None,errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
    #Log in with bad credentials
    def testLogin2(self):
	respData = self.makeRequest("/users/login", method="POST", data={'user':'user1', 'password':'password'*300})
	self.assertResponse(respData, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
    #Add an user, and then try to log in, should return success.
    def testLogin3(self):
	respData = self.makeRequest("/users/add", method="POST", data={'user':'wenhaocen', 'password': 'wenhaocen'})
	respData = self.makeRequest("/users/login", method="POST", data={'user':'wenhaocen','password':'wenhaocen'})
	self.assertResponse(respData, count=2,errCode = testLib.RestTestCase.SUCCESS)
    #Add an user with an empty password, and then login with the credentials. should return success
    def testLogin4(self):
	respData = self.makeRequest("/users/add", method="POST", data={'user':'wenhaocen', 'password': ''})
	respData = self.makeRequest("/users/login", method="POST", data={'user':'wenhaocen','password':''})
	self.assertResponse(respData, count=2,errCode = testLib.RestTestCase.SUCCESS)
    #Do a add user and then login regularly. should return success.
    def testLogin5(self):
	respData = self.makeRequest("/users/add", method="POST", data={'user':'wenhaocen', 'password': ''})
	respData = self.makeRequest("/users/login", method="POST", data={'user':'wenhaocen','password':''})
	self.assertResponse(respData, count=2,errCode = testLib.RestTestCase.SUCCESS)
	
	
    



    
