#!/usr/bin/env python 
#-------------------------------------------------------------------------------
# simple http wrapper
#-------------------------------------------------------------------------------

import base64
import urllib
import urllib2
import time
import re
import sys

class SendRequest:
  """
  SendRequest('http://xxx.com',data=dict, type='POST', auth='base',user='xxx', password='xxx')
  """
  def __init__(self, url, data=None, method='GET', auth=None, user=None, password=None, cookie = None, **header):
    """
    url: requested url, can not be null
    date: content need to be posted, must be dict
    method: Get OR Post, default Get
    auth: 'base' OR 'cookie'
    user: user name
    password: password
    cookie: cookie info
    e.g. referer='ca.msn.com'
    """

    self.url = url
    self.data = data
    self.method = method
    self.auth = auth
    self.user = user
    self.password = password
    self.cookie = cookie

    if 'referer' in header:
        self.referer = header[referer]
    else:
        self.referer = None

    if 'user-agent' in header:
        self.user_agent = header[user-agent]
    else:
## self.user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0'
        self.user_agent = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'

    self.__SetupRequest()
    self.__SendRequest()

  def __SetupRequest(self):

    if self.url is None or self.url == '':
        raise 'url cannot be NULL!!!'

    #set up access method
    if self.method.lower() == 'post':
        self.Req = urllib2.Request(self.url, urllib.urlencode(self.data))

    elif self.method.lower() == 'get':
        if self.data == None:
            self.Req = urllib2.Request(self.url)
        else:
            self.Req = urllib2.Request(self.url + '?' + urllib.urlencode(self.data))

    #set up auth info
    if self.auth == 'base':
        if self.user == None or self.password == None:
            raise 'The user or password was not given!'
        else:
            auth_info = base64.encodestring(self.user + ':' + self.password).replace('\n','')
            auth_info = 'Basic ' + auth_info
            self.Req.add_header("Authorization", auth_info)

    elif self.auth == 'cookie':
        if self.cookie == None:
            raise 'The cookie was not given!'
        else:
            self.Req.add_header("Cookie", self.cookie)


    if self.referer:
        self.Req.add_header('referer', self.referer)
    if self.user_agent:
        self.Req.add_header('user-agent', self.user_agent)


  def __SendRequest(self):

    try:
      self.Res = urllib2.urlopen(self.Req)
      self.source = self.Res.read()
      self.code = self.Res.getcode()
      self.head_dict = self.Res.info().dict
      self.Res.close()
    except:
      print "Error: HttpWrapper=>_SendRequest ", sys.exc_info()[1]


  def GetResponseCode(self):
    """
    get server response code(200 means success,404 site does not exist)
    """
    return self.code

  def GetSource(self):
    """
    get page source
    """
    if "source" in dir(self):
        return self.source
    return u''

  def GetHeaderInfo(self):
    """
    u'get header info'
    """
    return self.head_dict

  def GetCookie(self):
    """
    get return Cookie from server
    """
    if 'set-cookie' in self.head_dict:
      return self.head_dict['set-cookie']
    else:
      return None

  def GetContentType(self):
    """
    get content type
    """
    if 'content-type' in self.head_dict:
      return self.head_dict['content-type']
    else:
      return None

  def GetCharset(self):
    """
    try to get charset
    """
    contentType = self.GetContentType()
    if contentType is not None:
        index = contentType.find("charset")
        if index > 0:
           return contentType[index+8:]
    return None

  def GetExpiresTime(self):
    """
    get expires time
    """
    if 'expires' in self.head_dict:
      return self.head_dict['expires']
    else:
      return None

  def GetServerName(self):
    """
    get server name
    """
    if 'server' in self.head_dict:
      return self.head_dict['server']
    else:
      return None

__all__ = [SendRequest,]

if __name__ == '__main__':
    b = SendRequest("http://www.google.com")
    #print b.GetSource()