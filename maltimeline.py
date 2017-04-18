from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from datetime import date
import platform

from mal.timeline import get_user_list
from navbar import create_navbar


def create_app():
    app = Flask(__name__)
    create_navbar(app)
    Bootstrap(app)
    
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    
    
    @app.route('/')
    def hello_world():
        debug = platform.node() == "GEORGES-PC"
        return render_template("index.html", debug=debug)
    
    @app.route("/timeline")
    def timeline_redirect():
        if len(request.args.get('username', "")) > 0:
            return redirect(url_for("timeline", username=request.args.get('username')))
        else:
            return redirect(url_for("hello_world"))
    
    @app.route("/timeline/<string:username>")
    def timeline(username):
        try:
            user, anime_list, unlisted, earliest_start, years, seasons = get_user_list(username)
        except Exception:
            return redirect(url_for("hello_world"))
        
        return render_template("timeline.html", user=user, anime_list=anime_list, unlisted=unlisted, earliest_start=earliest_start, today=date.today(), years=years, seasons=seasons)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
