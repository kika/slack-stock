### Bot to report stock price to any Slack channel 
Sample implementation of Slack Webhook integration using Python and running on Google App Engine

There's no heavy dependency on App Engine. Just remove `import ... memcache` and replace `httplib2.Http(memcache)` with just `httplib2.Http()` and you can run this code on any WSGI app server.

Steps to configure:

1. Create Google App Engine project: https://console.developers.google.com
1. Call it whatever you want. Your integration point for slack would be either `http://<project-id>.appspot.com/price/<ticker>` or `http://<project-id>.appspot.com/price`. In the latter case you'd need to specify a ticker name or a list of ticker names when calling the bot on the channel.
1. Clone this repository
1. Run `pip install -r requirements.txt -t lib/ in app subdirectory`
1. Run `deploy.sh`
1. Test with curl: `curl -X POST -H "Content-Length: 0" http://<project-id>.appspot.com/price/AAPL`
1. Go to Integrations configuration in your Slack account
1. Configure the above URL as Outgoing Webhook
