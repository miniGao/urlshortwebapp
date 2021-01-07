# templates folder is used by flask to store web page files
# import render_template, this is powered by Jinja template engine
# import request to get access to http request information
# import redirect to redirect pages
# import url_for to make direct call to method in redirect
# when there is something wrong, "abort" sends back a special error message depending on what it is
# import cookies (session)
# import jsonify, it takes list, dictionary and turns them into json
# import Blueprint to use __init__
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

# __init__ #
# replace all app with bp, and url_for('~') to url_for('urlshort.~')
bp = Blueprint("urlshort", __name__)

@bp.route("/")
def home():
    # pass variable to template file
    return render_template("home.html", projectName="URL Shortener", codes = session.keys())

@bp.route("/about")
def about():
    return "This is a url shortener."

# Get request
# @app.route("/your-url")
# def your_url():
#     return render_template("your_url.html", code=request.args["code"])

# Post request
@bp.route("/your-url", methods=["GET", "POST"])
def your_url():
    if request.method == "POST":
        # create a dictionary key, url
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))

        # check if it's a file or url
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            # secure_filename checks for script injection
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('E:/Workspace/private-workspace/flask/url-shortener/urlshort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            # create cookie, session can be assigned with timestamp or other datatype as well
            session[request.form["code"]] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        # return "This is not valid"
        # return redirect("/")
        return redirect(url_for("urlshort.home"))

# after "/" catch string and put it into variable "code"
@bp.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists("urls.json"):
        with open("urls.json") as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if "url" in urls[code].keys():
                    return redirect(urls[code]["url"])
                else:
                    # get url for static file
                    return redirect(url_for("static", filename="user_files/" + urls[code]["file"]))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

# create JSON API
@bp.route("/api")
def session_api():
    return jsonify(list(session.keys()))