import os,random,string,cherrypy
import back_end

class MatteoWrapper(object):
    @cherrypy.expose
    def index(self):
        homepage_html_path = 'html\\home.html'
        cherrypy.session['home_html'] = open(homepage_html_path,'r').read()
        return cherrypy.session['home_html']

    @cherrypy.expose
    def handle_form(self, dicts, crits, query):
        cherrypy.session['query'] = query
        return back_end.run_matteo(cherrypy.session['query'],dicts,crits)

    @cherrypy.expose
    def display(self):
        return cherrypy.session['home_html']

if __name__ == '__main__':
    conf = {
                # For the root directory
                '/': 
                {
                    'tools.sessions.on': True
                },
                # For the img directory
                '/img': 
                {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
                }
            }
    print conf
    cherrypy.quickstart(MatteoWrapper(), '/', conf)