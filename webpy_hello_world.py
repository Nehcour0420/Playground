import web
        
urls = (
    '/(.*)', 'Index'
)
app = web.application(urls, globals())

web.config.debug = True

class Index: 

	def __init__(self):
		self.render = web.template.render('templates/')
		
    def GET(self, name=None):
		return self.render.index("Hello World")
	
	def POST(self, name):
		return "post"

if __name__ == "__main__":
    app.run()