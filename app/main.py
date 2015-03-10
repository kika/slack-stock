from bottle import Bottle
import httplib2
import json
from google.appengine.api import memcache

bottle = Bottle()

@bottle.route('/price/<ticker>', method='POST')
def price(ticker):
    query = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22$TICKER%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback=".replace("$TICKER", ticker)
    http = httplib2.Http(memcache)
    (headers,content) = http.request(query, "GET")
    resp = {}
    try:
        res = json.loads(content)['query']['results']['quote']["LastTradePriceOnly"]
        resp['text'] = res
    except:
        resp['text'] = "Unhandled error: " + sys.exc_info()[0]
    return resp


# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.'
