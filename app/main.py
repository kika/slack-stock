from bottle import Bottle,request
import httplib2
import json
from google.appengine.api import memcache

bottle = Bottle()
http = httplib2.Http(memcache)

def get_ticker(ticker):
    query = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22$TICKER%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback=".replace("$TICKER", ticker)
    (headers,content) = http.request(query, "GET")
    try:
        return json.loads(content)['query']['results']['quote']
    except:
        return "Unhandled error: " + sys.exc_info()[0]

def print_results(results):
    printable = []
    if not isinstance(results, list):
        results = [results]
    for result in results:
        printable.append( 
            "%s: %s" 
            % (result['symbol'], result['LastTradePriceOnly'])
        )
    return "\n".join(printable)

@bottle.route('/price/<ticker>', method='POST')
def price(ticker):
    return { 'text': print_results(get_ticker(ticker)) }

@bottle.route('/price', method='POST')
def parse():
    trig = request.forms.get('trigger_word')
    text = filter(lambda s: s != '',
                request.forms.get('text').replace(trig, "").replace(","," ").split()
            )
    return { 'text': print_results(get_ticker(",".join(text))) }

# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.'
