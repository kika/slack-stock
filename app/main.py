from bottle import Bottle,request
import httplib2
import json
from google.appengine.api import memcache
import logging

bottle = Bottle()
http = httplib2.Http(memcache)

def get_ticker(ticker):
    query = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from"   \
        "%20yahoo.finance.quotes%20where%20symbol%20in%20(%22$TICKER%22)%0A"  \
        "%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org" \
        "%2Falltables.env&callback=".replace("$TICKER", ticker)
    (headers,content) = http.request(query, "GET")
    if headers['status'] == '200':
            return json.loads(content)['query']['results']['quote']
    return "HTTP status: " + headers['status']

def print_results(req, results):
    printable = []
    change_total = 0
    if not isinstance(results, list):
        results = [results]
    for result in results:
        if isinstance(result,dict):
            printable.append( 
                "%s: %s" 
                % (result['symbol'], result['LastTradePriceOnly'])
            )
            if result['ChangeinPercent'] : 
                change_total += float(result['ChangeinPercent'].replace('%',''))
    status = 'rich' if change_total > 0 else 'poor'
    congrats = "\nYou're gonna be %s, @%s" % (status, req.forms.get('user_name'))
    return "\n".join(printable) + congrats

@bottle.route('/price/<ticker>', method='POST')
def price(ticker):
    return { 'text': print_results(request, get_ticker(ticker)) }

@bottle.route('/price', method='POST')
def parse():
    trig = request.forms.get('trigger_word')
    text = filter(lambda s: s != '',
                request.forms.get('text')
                .replace(trig, "")
                .replace(","," ")
                .split()
            )
    return { 
        'text': print_results(request, get_ticker(",".join(text))),
        'link_names': 1
        }

# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.'
