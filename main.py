import os,random,string,cherrypy
import back_end

class MatteoWrapper(object):
    @cherrypy.expose
    def index(self):
        homepage_html_path = 'html\\home.html'
        cherrypy.session['home_html'] = open(homepage_html_path,'r').read()
        return cherrypy.session['home_html']

    @cherrypy.expose
    def handle_form(self, **params):
        # Check for valid inputs
        # - query (empty query is accepted for now - it is a request to display all terms)
        query = params['query']
        # - dicts (empty dicts not accepted)
        try:
            dicts = params['dicts']
        except KeyError:
            return 'Error: You did not specify any dictionaries to search. Go back to home page to search again.'
        # - crits (empty crits not accepted)
        try:
            crits = params['crits']
        except KeyError:
            return 'Error: You did not specify any search criteria. Go back to home page to search again.'
        return back_end.run_matteo(query,dicts,crits)

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
    print "===Welcome to MATTEO! You may go to http://localhost:8080 in your browser now==="
    cherrypy.quickstart(MatteoWrapper(), '/', conf)