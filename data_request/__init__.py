from theophanie_models.life import Life as LifeMessage, LifeType

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
  authors_part = LifeMessage(text="Authors", value=str(__authors__), type=LifeType.INFO)
  licence_part = LifeMessage(text="Licence", value=__short_licence_name__, type=LifeType.INFO)
  version_part = LifeMessage(text="Version", value=__version__, type=LifeType.INFO)
  life_message = LifeMessage(text=__name__, children=[version_part, authors_part, licence_part], type=LifeType.INFO)

  return life_message