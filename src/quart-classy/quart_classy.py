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

  decorators = []

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

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

  def register(self, app):
    _class_name = self._get_self_name()

    if "view" in _class_name.lower():
      _class_name = _class_name[:-4]
    
    if not self.url_prefix:
      self.url_prefix = f"/{_class_name}"
    
    if _class_name.lower() == "root":
      self.url_prefix = ""
    
    _methods = self._get_method_names()

    for _method in _methods:
      if _method == "index":
        _route = f"{self.url_prefix}/"
      else:
        _route = f"{self.url_prefix}/{_method}/"
      
      _obj_class  = self
      _obj_method = getattr(self, _method)

      if self.decorators:
        for _decorator in reversed(self.decorators):
          _obj_method = _decorator(_obj_method)

      print(f"==> Registering {_route}")
      app.add_url_rule(_route, endpoint=_route, view_func=_obj_method)
      