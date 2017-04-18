from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Text, Separator, NavigationItem
from flask_nav.renderers import SimpleRenderer
from flask_nav import register_renderer
from dominate import tags
from flask_bootstrap.nav import BootstrapRenderer

def create_navbar(app):
    nav = Nav()
    nav.init_app(app)
    
    class TextInput():
        pass

    class CustomRenderer(BootstrapRenderer):
        def visit_TextInput(self, node):
            x = tags.form(
                    tags.div(
                        tags.input(_type="text", _class="form-control", placeholder="Search MAL usernames", name="username"),
                    tags.span(
                        tags.button(tags.span(_class="glyphicon glyphicon-search"), _type="submit", _class="btn btn-default"),
                        _class="input-group-btn"),
                    _class="input-group"),
            action="/timeline",
            method="get",
            _class="navbar-form navbar-left")
            return x
        
    register_renderer(app, "custom_renderer", CustomRenderer)
    
    @nav.navigation()
    def nav_bar_renderer():
        navbar = Navbar("maltimeline",
                        View("Index", "hello_world"),
                        TextInput(),)
        #html = navbar.render()
        #html = html.replace("navbar navbar-default", "navbar navbar-inverse navbar-fixed-top")
        #navbar.render = lambda: html
        return navbar