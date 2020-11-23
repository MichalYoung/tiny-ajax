"""
Simple Flask web site 
"""
import flask  # The basic framework for http requests, storing cookies, etc
import logging  # For monitoring and debugging

###
# Globals
###

import config  # Separate out per-machine configuration

app = flask.Flask(__name__)
app.secret_key = config.COOKIE_KEY
app.debug = config.DEBUG
app.logger.setLevel(logging.DEBUG)


#################
# Pages and request handling:
# We "route" URLs to functions by attaching
# the app.route 'decorator'.
#################

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('form.html')

###################
#  Ajax routes ---
#     these take and produce JSON structures
###################

@app.route("/_ajax_url")
def ajax_url_handler():
    sent_value = flask.request.args.get("value", type=int)
    try:
        v = int(sent_value)
    except:
        v = 0;
    doubled = v * 2;
    tripled = v * 3;
    rslt = {"doubled": doubled, "tripled": tripled}
    return flask.jsonify(result=rslt)

###################
#   Error handlers
#   These are pages we display when something goes wrong
###################
@app.errorhandler(404)
def error_404(e):
    app.logger.warning("++ 404 error: {}".format(e))
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    app.logger.warning("++ 500 error: {}".format(e))
    assert app.debug == False  ## Crash me please, so I can debug!
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def error_403(e):
    app.logger.warning("++ 403 error: {}".format(e))
    return flask.render_template('403.html'), 403


#############
# Filters
# These process some text before inserting into a page
#############
@app.template_filter('humanize')
def humanize(date):
    """Humanize an ISO date string"""
    as_arrow = arrow.get(date)
    return as_arrow.humanize()


# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#
if __name__ == "__main__":
    # Running standalone
    print("Opening for global access on port {}".format(config.PORT))
    app.run(port=config.PORT, host="0.0.0.0")

# We could also be running from the gunicorn WSGI server,
# which makes the call to app.run.  Gunicorn may invoke more than
# one instance for concurrent service, so make sure the application
# is thread safe!
