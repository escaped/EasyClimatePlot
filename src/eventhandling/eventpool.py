from event import Event

class EventPool (object):
  '''A datastructure that contains subscribable events.'''
  def __init__ (self):
    self.events = {}

  def __getitem__ (self, key):
    try:
      return self.events[key]
    except KeyError:
      self.events[key] = Event ()
      return self.events[key]
