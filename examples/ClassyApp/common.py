# ~
# Decorators
# ~

def one(f):
  def decorator(*args, **kwargs):
    print("==> Hello from decorator one.")
    return f(*args, **kwargs)
  return decorator

def two(f):
  def decorator(*args, **kwargs):
    print("==> Hello from decorator two.")
    return f(*args, **kwargs)
  return decorator
