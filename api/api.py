import os
from tornado.web import RequestHandler
from tornado import template

def render_string(template_name, **kwargs):
    """Generate the given template with the given arguments.

    We return the generated string. To generate and write a template
    as a response, use render() above.
    """
    # If no template_path is specified, use the path of the calling file
    template_path=os.path.join(os.path.dirname(__file__), "templates")
    template_path="/Users/vladimir/PycharmProjects/my-chat2/templates"
    if not getattr(RequestHandler, "_templates", None):
        RequestHandler._templates = {}
    if template_path not in RequestHandler._templates:
        loader = template.Loader(template_path)
        RequestHandler._templates[template_path] = loader
    t = RequestHandler._templates[template_path].load(template_name)
    args = dict(
    )
    args.update(kwargs)
    return t.generate(**args)
