from quart_classy import ClassyBlueprint
from common import *

class RootView(ClassyBlueprint):
  
  async def index(self):
    return "Root index"
  
  async def another_view(self):
    return "/ another_view"