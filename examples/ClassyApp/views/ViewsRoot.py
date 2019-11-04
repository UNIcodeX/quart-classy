from quart_classy import ClassyBlueprint
from common import *

class RootView(ClassyBlueprint):
  
  async def index(self):
    return "Root index"

  async def get(self, id):
    id = int(id)
    if id:
      return f"got ID {id}"
    else:
      return "No ID", 404
  
  async def another(self):
    return "/ another_view"