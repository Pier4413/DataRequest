from theophanie_models.life import Life as LifeMessage

__name__ = "Data Request"
__authors__ = ["Panda <panda@delmasweb.net>"]
__short_licence_name__ = "No licence"
__long_licence_text__ = ""
__version__ = "1.0.0"

def create_life_message() -> LifeMessage:

  """
    Create the life message in the format of models

    :rtype: LifeMessage
  """
  authors_part = LifeMessage(text="Authors", value=str(__authors__))
  licence_part = LifeMessage(text="Licence", value=__short_licence_name__)
  version_part = LifeMessage(text="Version", value=__version__)
  life_message = LifeMessage(text=__name__, childs=[version_part, authors_part, licence_part])

  return life_message