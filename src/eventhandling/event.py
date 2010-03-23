'''This module provides simple event handling via callable objects.'''

# see http://www.valuedlessons.com/2008/04/events-in-python.html
# TODO License?
class Event:
  def __init__(self):
    self.handlers = set()

  def handle(self, handler):
    self.handlers.add(handler)
    return self

  def unhandle(self, handler):
    try:
        self.handlers.remove(handler)
    except:
        raise ValueError("Handler is not handling this event, so cannot unhandle it.")
    return self

  def fire(self, *args, **kargs):
    '''Fire returns True, if every handler returns True.'''
    value = True
    for handler in self.handlers:
      val = handler(*args, **kargs)
      if not val and value: value = False

    return value

  def getHandlerCount(self):
    return len(self.handlers)

  __iadd__ = handle
  __isub__ = unhandle
  __call__ = fire
  __len__  = getHandlerCount
