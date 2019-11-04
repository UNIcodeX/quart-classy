from random import choice

from quart import Quart, redirect, url_for
from quart_classy import ClassyBlueprint

quotes = [
  "The secret of getting ahead is getting started. ~ Mark Twain",
  "The scientific man does not aim at an immediate result. ~ Nikola Tesla",
  "Always remember that you are absolutely unique. Just like everyone else. ~ Margaret Mead"
]

app = Quart(__name__)

class QuotesView(ClassyBlueprint):
  url_prefix="/Quotes"

  def index(self):
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
  
  async def redir(self):
    return redirect(url_for("QuotesView.get", id=2))

QuotesView().register(app, url_prefix="quotes")

if __name__ == '__main__':
  app.run()