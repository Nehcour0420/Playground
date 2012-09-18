import web
import random
import string
import pymongo
import urlparse

render = web.template.render('templates/')
urls = (
    '/', 'index',
    '/(.*)', 'redirect',
)

app = web.application(urls, globals())

connection = Connection('localhost', 27017)

class index:
    def GET(self):
        return render.index(url=None, shortcode=None)
    
    def POST(self):
        i = web.input()
        url = i.url
        if urlparse.urlparse(url)[0] == '' and urlparse.urlparse(url)[1] == '':
            return render.index(url=None, shortcode=None, err="error")
        else:
            shortcode = connection.get("shortcode:%s" % url)
            print 'shortcode:%s' % shortcode
            if shortcode == None:
                while True:
                    shortcode = ''.join(random.choice(string.letters + string.digits) for x in range(6))
                    if connection.get("url:%s" % shortcode) == None:
                        connection.set("url:%s" % shortcode, url)
                        connection.set("shortcode:%s" % url, shortcode)
                        break
            return render.index(url=url, shortcode=shortcode)

class redirect:
    def GET(self, shortcode):
        url = connection.get("url:%s" % shortcode)
        if url != None:
            raise web.seeother(url)

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()