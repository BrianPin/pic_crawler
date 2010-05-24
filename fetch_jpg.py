""" A web photo, picture grabber """
import sys
import urllib
import urllib2
from HTMLParser import HTMLParser

'''
The WretchWebParser is used to parse the content HTML of wretch.cc
'''
class WretchWebParser(HTMLParser):
  """ HTML page filter to get photo information
  """
  def __init__(self):
    HTMLParser.__init__(self)
    self.photo_url_list = []

  def reset(self):
    # new style not suitable here?  super(PhotoWebParser, self).reset()
    HTMLParser.reset(self)
    self.photo_url_list = []

  def handle_starttag(self, tag, attrs):
    print "tag %s"%(tag)
    if tag == 'img':
      for k,v in attrs:
        print "(%s->%s)"%(k,v)

  def handle_data(self, data):
    #print "meet data %s"%(data)
    pass

'''
The PbaseWebParser is used to parse the content HTML of pbase.com
''' 
class PbaseWebParser(HTMLParser):
  """ HTML page filter to get photo information
  """
  def __init__(self):
    HTMLParser.__init__(self)
    self.photo_url_list = []
    self.img_src_list = []
    self.found_end_node = 0

  def reset(self):
    # new style not suitable here?  super(PhotoWebParser, self).reset()
    HTMLParser.reset(self)
    self.photo_url_list = []
    self.img_src_list = []
    self.found_end_node = 0

  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      tag_dict = {}
      for k,v in attrs:
        tag_dict[k] = v
      if 'class' in tag_dict and tag_dict['class'] == 'thumbnail':
        #print "img in %s"%(tag_dict['href'])
        self.photo_url_list.append(tag_dict['href'])
    if tag == 'img':
      tag_dict = {}
      for k,v in attrs:
        tag_dict[k] = v
      if 'class' in tag_dict and tag_dict['class'] == 'display':
        self.img_src_list.append(tag_dict['src'])
        self.found_end_node = 1

  def handle_data(self, data):
    #print "meet data %s"%(data)
    pass


def build_url(url_link, enc_data=None):
  try:
    request = urllib2.Request(url_link, enc_data)
    request.add_header('Referer', 'http://www.wretch.cc')
    request.add_header('User-Agent', 'Mozilla 5.0')
    response = urllib2.urlopen(request)
  except urllib2.URLError:
    print "The %s is not valid URL\n"%(url_link)
  except ValueError:
    print "The %s is not valid URL\n"%(url_link)
  else:
    return response
  return None


def bfs_search_pbase(url, data=None):
  webparser = PbaseWebParser()
  res = build_url(url, data)
  if res != None:
    html = res.read()
    webparser.feed(html)
    if webparser.found_end_node == 0:
      for link in webparser.photo_url_list:
        bfs_search_pbase(link)
    else:
      print webparser.img_src_list
  else:
    print "Nothing returned from URL fetcher\n"


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: python fetch_jpg.py YOUR_URL"
  else:
    import re
    inp_dict = None
    inp_data = None
    inpurl = sys.argv[1]
    webparser = None
    
    # The following code can be extended to accept new sites
    # 1. add the site name in the following sites tuple
    # 2. adds code to prepare for the query for that site
    # 3. site names in sites tuple can not have duplicates
    sites = ('wretch', 'pbase')
    for site in sites:
      ret = re.search(site, inpurl)
      if ret != None and site == 'wretch':
        name_id = sys.argv[2]
        book_id = sys.argv[3]
        inp_dict = {}
        inp_dict[name_id] = book_id
        inp_data = urllib.urlencode(inp_dict)
        webparser = WretchWebParser()
        res = build_url(inpurl, inp_data)
        if res != None:
          html = res.read()
          if webparser != None:
            webparser.feed(html)
            print webparser.photo_url_list
          else:
            print "No parser for %s"%(inpurl)
        else:
          print "Nothing returned from URL fetcher\n"

      if ret != None and site == 'pbase':
        bfs_search_pbase(inpurl)
