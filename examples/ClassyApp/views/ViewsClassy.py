from quart_classy import ClassyBlueprint
from common import *

class ClassyView(ClassyBlueprint):
  decorators = [one, two]
  
  async def index(self):
    return "ClassyView index"

  async def another_view(self):
    return "ClassyView / another_view"
