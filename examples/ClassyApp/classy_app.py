from quart import Quart
from views.ViewsRoot import RootView
from views.ViewsClassy import ClassyView

app = Quart(__name__)

RootView("Root", __name__, url_prefix="/").register(app)
ClassyView("Classy", __name__, url_prefix="/classy").register(app)

# OR
# classy_view = ClassyView("Classy", __name__, url_prefix="/Classy")
# classy_view.register(app)

if __name__ == "__main__":
  app.run()