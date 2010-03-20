# -*- coding: utf-8 -*-
class Hook:
  '''Hook is an abstract base class implementing basic functions used by the
  workflow panel. NOTE: Every panel which is added to a workflow should inherit this
  class!'''

  def deactivate (self):
    '''things to do before switching this panel. Returns true if switching is forbidden
    (e.g. because of missing values).'''
    return True

  def activate (self):
    '''Things to do after switching to this panel. Returns false if something went wrong
    (for example if the last panel missed some values).'''
    return True
