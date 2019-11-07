"""
  Quart-Classy
  ------------

  Class based views for the Quart microframework.

  Extends functionality of Blueprints to auto-magically create routes for
  methods defined within a Class which inherits from ClassyBlueprint.

  :copyright: (c) 2019 by Jared Fields (UNIcodeX).
  :license: BSD, see LICENSE for more details.
"""

__version__ = "0.0.1"

from typing import Optional, List, Callable
from functools import wraps

from quart import Blueprint

IGNORED_METHODS = [
  '__class__', '__delattr__', '__dir__', '__eq__', '__format__', '__ge__',
  '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__',
  '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
  '_find_root_path', 'add_app_template_filter', 'add_app_template_global',
  'add_app_template_test', 'add_url_rule', 'add_websocket', 
  'after_app_request', 'after_app_websocket', 'after_request', 
  'after_websocket', 'app_context_processor', 'app_errorhandler', 
  'app_template_filter', 'app_template_global', 'app_template_test', 
  'app_url_defaults', 'app_url_value_preprocessor', 'before_app_first_request',
  'before_app_request', 'before_app_websocket', 'before_request', 
  'before_websocket', 'context_processor', 'endpoint', 'errorhandler', 
  'get_send_file_max_age', 'make_setup_state', 'open_resource', 'record', 
  'record_once', 'register', 'register_error_handler', 'route', 
  'send_static_file', 'teardown_app_request', 'teardown_request', 
  'teardown_websocket', 'test', 'url_defaults', 'url_value_preprocessor', 
  'websocket'
]


class ClassyBlueprint(Blueprint):
  
  url_prefix = ""
  decorators = []
  subdomain  = None
  _custom_routes = dict()

  def __init__(self, *args, **kwargs):
    self._derive_info()
    
    # Set appropriate defaults in case View was lazily initialized:
    # i.e. ClassyView().register(app) 
    #      ~~ rather than ~~
    #      ClassyView("Classy", __name__, ...)

    # If only one positional argument is given, find out which it is and set a sane
    # default for the other. Set sane defaults for both, if none are defined.
    if args and len(args) < 2:
      _list_args = list()
      for _arg in args:
        if "__" not in _arg:
          args = tuple([args[0], __name__])
        else:
          args = tuple([self._class_name , args[0]])
    elif not args:
      args = tuple([self._class_name , __name__])

    if self.url_prefix:
      kwargs['url_prefix'] = self.url_prefix

    super().__init__(*args, **kwargs)
  
  def _derive_info(self):
    self._class_name_full = self._get_self_name()

    if "view" in self._class_name_full.lower():
      self._class_name = self._class_name_full[:-4]
    
    if not self.url_prefix:
      self.url_prefix = f"/{self._class_name}"
    
    if self._class_name.lower() == "root":
      self.url_prefix = ""
  
  @classmethod
  def route(cls, 
    path: str,
    methods: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    defaults: Optional[dict] = None,
    host: Optional[str] = None,
    subdomain: Optional[str] = None,
    *,
    provide_automatic_options: Optional[bool] = None,
    strict_slashes: bool = True
  ) -> Callable:
    def decorator(func: Callable) -> Callable:
      cls._custom_routes[func.__name__] = dict()
      cls._custom_routes[func.__name__]['path'] = path
      cls._custom_routes[func.__name__]['methods'] = methods
      cls._custom_routes[func.__name__]['endpoint'] = endpoint
      cls._custom_routes[func.__name__]['defaults'] = defaults
      cls._custom_routes[func.__name__]['host'] = host
      cls._custom_routes[func.__name__]['subdomain'] = subdomain
      cls._custom_routes[func.__name__]['provide_automatic_options'] = provide_automatic_options
      cls._custom_routes[func.__name__]['strict_slashes'] = strict_slashes
      return func
    return decorator

  @classmethod
  def _get_method_names(cls):
    methods = [
      func for func in dir(cls)
      if callable(getattr(cls, func))
      and func not in IGNORED_METHODS
      and str(func)[0] != "_"
    ]
    return methods
  
  @classmethod
  def _get_self_name(cls):
    return cls.__name__

  def register(self, app, url_prefix=""):
    _methods = self._get_method_names()
    if url_prefix:
      self.url_prefix = url_prefix

    self._derive_info()
    
    if self.url_prefix:
      if self.url_prefix[0] != '/':
        self.url_prefix = '/' + self.url_prefix

    # Generate routes
    for _method in _methods:
      # get the objects for the class and method names
      _obj_class  = self
      _obj_method = getattr(self, _method)
      _http_methods = None

      # Generate prefix and base
      if _method == "index":
        _route = f"{self.url_prefix}/"
      else:
        _route = f"{self.url_prefix}/{_method}/"

      # If ClassyBlueprint.route() decorator was used, then set vars accordingly
      if _method in self._custom_routes:
        args = self._custom_routes[_method]
        _route = self.url_prefix + args['path']
        _endpoint = args['endpoint']
        _http_methods = args['methods']
        self.subdomain = args['subdomain']

      # Handle possible arguments
      if _obj_method.__code__.co_argcount > 1:
        _arguments = tuple(val for val in _obj_method.__code__.co_varnames if val != 'self')
        app.logger.debug(f"==> Quart-Classy | {self._class_name_full}.{_method} has argument(s): {', '.join(_arguments)}")
        for _arg in _arguments:
          _route += "<" + _arg + ">/"

      # Apply decorators
      if self.decorators:
        for _decorator in reversed(self.decorators):
          _obj_method = _decorator(_obj_method)

      # if the method name is "get" then we strip it out
      if _method == "get":
        _route = _route.replace("get/", "")
      
      # Same for "post", but set HTTP method to 'POST'
      if _method == "post":
        _route = _route.replace("post/", "")
        _http_methods = ['POST']
      
      # Ensure there are no double slashes
      _route    = _route.replace("//", "/")
      _endpoint = self._class_name_full + "." + _method
      
      # Register the route
      app.logger.debug(f"==> Quart-Classy | Registering {_endpoint} as {_route}, with HTTP methods {_http_methods}")
      app.add_url_rule(_route, endpoint=_endpoint, view_func=_obj_method, methods=_http_methods, subdomain=self.subdomain)
