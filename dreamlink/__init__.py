from flask import Flask
from os.path import join
from dreamlink.page.dashboard import blueprint as dashboard_blueprint
from dreamlink.page.home import blueprint as home_blueprint
from dreamlink.page.login import blueprint as login_blueprint
from dreamlink.page.sign_up import blueprint as sign_up_blueprint
from dreamlink.page.nexus import blueprint as nexus_blueprint
from dreamlink.lib.root import root_directory

app = Flask(
    __name__,
    static_folder = join(root_directory, "assets"),
    static_url_path = "/assets/"
)

app.register_blueprint(dashboard_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(sign_up_blueprint)
app.register_blueprint(nexus_blueprint)

__all__ = ["app"]