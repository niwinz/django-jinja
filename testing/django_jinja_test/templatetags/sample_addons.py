from django_jinja import library
import jinja2


@library.test(name="one")
def is_one(n):
    return n == 1


@library.filter
@jinja2.contextfilter
def replace(context, value, x, y):
    return value.replace(x, y)


@library.global_function
def myecho(data):
    return data


@library.global_function
@library.render_with("test-render-with.jinja")
def myrenderwith(*args, **kwargs):
    return {"name": "Foo"}
