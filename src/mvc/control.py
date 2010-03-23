import eventhandling.eventpool

class Control (object):
  '''Abstract class, whose deriving classes should be used as controllers in MVC'''

  def __init__ (self, view):
    '''Constructor. view must be of type eventpool!'''
    if not isinstance (view, eventhandling.eventpool.EventPool):
      raise TypeError, "view must be of type EventPool!"

    self.view = view

    # subsribe to the events of the view
    # NOTE: we have to subscribe to EVERY GIVEN EVENT!
    self.__subscribe__ ()

  def __subscribe__ (self):
    for key, event in self.view.events.items ():
      try:
        event += getattr (self, "on" + key)
      except AttributeError:
        # TODO debugging facility
        print "please implement on%s for event %s" %(key, key)

