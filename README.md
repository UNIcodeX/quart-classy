Quart-Classy
=============

**NOTE! This is currently a work-in-progress, and breaking changes may be introduced.**

> 2019-11-04: Ended up rewriting to make use of Quart's Blueprints. 

> 2019-10-30: This repository was forked from [Flask-Classy](http://github.com/apiguy/flask-classy) by [@apiguy](https://twitter.com/APIguy). The goal of this project is to recreate Flask-Classy for the asynchronous reimplementation of
Flask, named [Quart](https://gitlab.com/pgjones/quart), which is the work of [Phil Jones](https://gitlab.com/pgjones).

Quart-Classy is an extension that adds class-based views to Quart. `Quart-Classy` will automatically generate routes based on the methods
in your views.

# Installation

Install the extension with:

```
$ pip install quart-classy
```

# How it Works

```python
from random import choice

from quart import Quart
from quart_classy import ClassyBlueprint

quotes = [
  "The secret of getting ahead is getting started. ~ Mark Twain",
  "The scientific man does not aim at an immediate result. ~ Nikola Tesla",
  "Always remember that you are absolutely unique. Just like everyone else. ~ Margaret Mead"
]

app = Quart(__name__)

class QuotesView(ClassyBlueprint):
  # Any Quart-Classy view which ends with `view` will have `view` stripped off

  def index(self):
    # Quart-Classy will automatically set the class' `index` method
    # as the root of that route.
    # `/Quotes/` rather than `/Quotes/index/`
    return "<br/>".join(quotes)
  
  def get(self, id):
    # Quart-Classy, changes "get" routes automatically
    # `/quotes/get/<id>` becomes `/quotes/<id>`
    id = int(id) -1
    if id <= len(quotes) and not id < 0:
      return quotes[id]
    else:
      return "Invalid index."
  
  def random(self):
    return choice(quotes)

QuotesView().register(app)
# ~OR~
# quotes_view = QuotesView()
# quotes_view.register(app)

if __name__ == '__main__':
  app.run()
```

Run this app and open your web browser to: [`http://localhost:5000/quotes/`](http://localhost:5000/quotes/)

Quart-Classy will automatically create routes for any method
in a ClassyBlueprint that doesn't begin with an underscore character.
You can still define your own routes of course, and we'll look at that next.

# Specifying a URL Prefix

A URL prefix is a great way to define a common base to urls. For example lets
say you had a bunch of views that were all part of your application's api system.

You *could* write custom route bases for all of them, but if you want to use
Quart Classy's automatic route generation stuff you'll lose
the part where it infers the route base from the name of the class.

A better choice is to use a URL prefix.

You can specify a URL prefix either as an attribute of the ClassyBlueprint, or when you register the ClassyBlueprint with the application.

## **As an attribute:**

Using an attribute is a great way to define a default prefix, as you can always
override this value when you register the ClassyBlueprint with your app:

```python
  class SquareView(ClassyBlueprint):
    url_prefix = "/shapes"

    def index(self):
      ...
```

## **When Registering:**

Alternatively (or additionally, if you like) you can specify a URL prefix when
you register the route with your app:

```python
SquareView(url_prefix="/shapes").register(app)
```

And this will override any URL prefixes set on the ClassyBlueprint class itself.

There are 3 ways to customize the prefix of a `ClassyBlueprint`.

Method 1
---
Change the name of the class

Method 2
---

Set the `url_prefix` attribute on your `ClassyBlueprint`. Suppose we wanted to make our QuotesView handle the root of the web application::

```python
class QuotesView(ClassyBlueprint):
  url_prefix = '/'

  def index(self):
    ...
```

Method 3
---

This method is perfect for when you're using app factories, and you need to be able to specify different base routes for different apps. You can specify the route when you register the class with the Quart app instance.

```python
QuotesView().register(app, route_base='/')
```

The second method will override the first, and the third method will always override the second, so you can use one method, and override it with another if needed.

# Specifying Custom Endpoints

To be written.

# Special method names

`ClassyBlueprint` will look for special methods in your class. I know that sometimes you just want things to just *work* and not have to think about it. Let's look at `ClassyBlueprint`'s special method names:

**index**
    *index* is generally used for home pages
    and lists of resources. The automatically generated route is:

    ============ ================================
    **rule**     /
    **endpoint** <class name>:index
    **method**   GET
    ============ ================================

**get**
    Another old familiar friend, `get` is usually used to retrieve a
    specific resource. The automatically generated route is:

    ============ ================================
    **rule**     /<id>
    **endpoint** <class name>:get
    **method**   GET
    ============ ================================

**post**
    This method is generally used for creating new instances of a resource
    but can really be used to handle any posted data you want. The
    automatically generated route is:

    ============ ================================
    **rule**     /
    **endpoint** <class name>:post
    **method**   POST
    ============ ================================

**put** To be written.

**patch** To be written.

**delete** To be written.

# url_for()

Once you've got your `ClassyBlueprint` registered, you'll probably want to be able to get the urls for it in your templates and redirects and whatnot. Quart
ships with the awesome `url_for` function that does an excellent job of
turning a function name into a url that maps to it. You can use `url_for`
with Quart-Classy by using the format `<Class name>.<method name>`.

```python
class QuotesView(ClassyBlueprint):
  def index(self):
    return "<br/>".join(quotes)

  def get(self, id):
    id = int(id) -1
    if id <= len(quotes) and not id < 0:
      return quotes[id]
    else:
      return "Invalid index."

  def random(self):
    return choice(quotes)
```

In this example, you can get a url to the index method using

```python
    url_for("QuotesView.index")
```

And you can get a url to the get method using

```python
    url_for("QuotesView.get", id=2)
```
> NOTE: Notice that the custom endpoint does not get prefixed with the class
  name like the auto-generated endpoints. When you define a custom endpoint, we hand that over to Quart in it's original, unaltered form.

# Your own methods

If you add your own methods `ClassyBlueprint` will detect them during registration and register routes for them, whether you've gone and defined your own, or you just want to let `ClassyBlueprint` do it's thing. By default, `ClassyBlueprint` will create a route that is the same as the method name.

```python
class SomeView(ClassyBlueprint):

  def my_view(self):
    return "Check out my view!"
```

`ClassyBlueprint` will generate a route like this:

```
============ ================================
**rule**      /Some/my_view/
**endpoint**  SomeView.my_view
**method**    GET
============ ================================
```

"That's fine." you say. "But what if I have a view method with some
parameters?" Well `ClassyBlueprint` will try to take care of that for you
too. If you were to define another view like this::

```python
class AnotherView(ClassyBlueprint):
  url_prefix = "/home"

  def this_view(self, arg1, arg2):
    return "Args: %s, %s" % (arg1, arg2,)
```

`ClassyBlueprint` would generate a route like this:

```
============ ================================
**rule**     /home/this_view/<arg1>/<arg2>
**endpoint** AnotherView.this_view
**method**   GET
============ ================================
```

> NOTE: One important thing to note, is that `ClassyBlueprint` does not type your parameters.

# Decorators

For `ClassyBlueprint` all you need to do is add a `decorators` attribute to the
class definition with a list of decorators you want applied to every method and `Quart-Classy` will take care of the rest.

```python
class WhataGreatView(ClassyBlueprint):
  decorators = [login_required]

  def this_is_secret(self):
    return "If you see this, you're logged in."

  def so_is_this(self):
    return "Looking at me? I guess you're logged in."
```

# `@app.before_reqeust` and `@app.after_request`

To be written.

# Subdomains

By now, you've built a few hundred `Quart` apps using `Quart-Classy`
and you probably think you're an expert. But not until you've tried
the snazzy `Subdomains` feature my friend.

Quart-Classy allows you to specify a subdomain to be used when
registering routes for your ClassyBlueprints. While the usefulness of this
feature is probably apparent to many of you, let's go ahead and take a
look at one of the many facilitative use cases.

Suppose you've got a sweet api you're porting over from a legacy app
and in the migration you want to clean things up a bit and start using
a subdomain like ``api.socool.biz`` instead of the old way of accessing
it using ``api`` at the root of the path like ``socool.biz/api``. The
only catch, of course, is that you have api clients still using that
old path based method. What is a hard working developer like you to do?

Thanks to `Quart` and `Quart-Classy` you have some options. There are two
easy ways you can choose from to tell `Quart-Classy` which subdomains your
``ClassyBlueprint`` should respond to.

Let's see both methods so you can choose which one works best for your
application.

Define During Registration
---

Probably the most flexible method, you can define which subdomains you
want to support at the same time you're registering your views::

```python
# views.py
from quart_classy import ClassyBlueprint

class CoolApiView(ClassyBlueprint):

  def index(self):
    return "API stuff"
```

```python
# main.py
from quart import Quart
from views import CoolApiView

app = Quart(__name__)
app.config['SERVER_NAME'] = 'socool.biz'

# This one matches urls like: http://socool.biz/api/...
CoolApiView.register(app, route_base='/api/')

# This one matches urls like: http://api.socool.biz/...
CoolApiView.register(app, route_base='/', subdomain='api')

if __name__ == "__main__":
  app.run()
```

Define in the Class
---

Using this method, you can explicitly define a subdomain as an attribute of
the ``ClassyBlueprint`` subclass.
```python
# views.py

from quart_classy import ClassyBlueprint

class CoolApiView(ClassyBlueprint):
  subdomain = "api"

  def index(self):
    return "API Stuff"
```

```python
# main.py

from quart import Quart
from views import CoolApiView

app = Quart(__name__)
app.config['SERVER_NAME'] = 'socool.biz'

# This one matches urls like: http://socool.biz/api/...
CoolApiView.register(app, route_base='/api/', subdomain='')

# This one matches urls like: http://api.socool.biz/...
CoolApiView.register(app, route_base="/")

if __name__ == "__main__":
  app.run()
```

As you can see here, specifying the subdomain to the register method will
override the explicit subdomain attribute set inside the class.

# Questions?

Message me on GitHub, email [jbcomps@gmail.com](mailto:jbcomps@gmail.com), or catch me on Keybase ([jared_fields](https://keybase.io/jared_fields/))

Pull requests are welcome.

# Thanks go out to...

- Armin Ronacher, who created Flask.
- Phil Jones, who ported Flask to be asynchronous, in Quart.
- Freedom Dumlao for creating Flask-Classy, which is the inspiration for this project.

---

© Quart-Classy Copyright 2019 by Jared Fields.
