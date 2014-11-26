.. image:: https://travis-ci.org/davemenninger/reconcile-worldcat-demo.svg?branch=master
    :target: https://travis-ci.org/davemenninger/reconcile-worldcat-demo

A demo Google Refine reconciliation service API.

Does a title search using Worldcat Search API.

Here's how to make this work on heroku. ( https://devcenter.heroku.com/articles/getting-started-with-python ):

* git clone https://github.com/davemenninger/reconcile-worldcat-demo.git

* cd reconcile-worldcat-demo

* heroku login

* virtualenv venv

* source venv/bin/active

* [put your worldcat api key into a file called .env like WSKEY=yourapikey12345blah]

* heroku create

* heroku config:push

* git push heroku master

If you want to get it to run locally for testing, you'll need to do:

* pip install -r requirements.txt

* foreman start
