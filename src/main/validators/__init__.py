import wx
from wxcustom.error import ErrorMessage

class TextCtrlValidator (wx.PyValidator):
  def __init__(self, canEmpty = True):
    """ Standard constructor.
    """
    wx.PyValidator.__init__(self)
    self.errorMessage = ""
    self.canEmpty = canEmpty
    
  def TransferToWindow(self):
    """ Transfer data from validator to window.
        The default implementation returns False, indicating that an error
        occurred.  We simply return True, as we don't do any data transfer.
    """
    return True # Prevent wxDialog from complaining.

  def TransferFromWindow(self):
    """ Transfer data from window to validator.
        The default implementation returns False, indicating that an error
        occurred.  We simply return True, as we don't do any data transfer.
    """
    return True # Prevent wxDialog from complaining.
    
  def Clone(self):
    """ Standard cloner.
        Note that every validator must implement the Clone() method.
    """
    return TextCtrlValidator(self.canEmpty)
  
  def checkValue(self, v):
    if not self.canEmpty and len(v) == 0:
      self.errorMessage = "Field cannot be empty"
      return False
    return True
  
  def Validate(self, win):
    self.errorMessage = ""
    textCtrl = self.GetWindow()
    value = textCtrl.GetValue()
    
    if not self.checkValue(value):
      ErrorMessage (self.errorMessage)
      textCtrl.SetBackgroundColour("pink") # does not work
      textCtrl.SetFocus()
      textCtrl.Refresh()
      return False
    
    textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
    textCtrl.Refresh()
    return True
  
class NumberValidator (TextCtrlValidator):
  def __init__(self, range = None, canEmpty = True):
    TextCtrlValidator.__init__(self, canEmpty)
    self.range = range
    
  def Clone(self):
    return NumberValidator(self.range, self.canEmpty)
  
  def checkValue(self, v):
    if TextCtrlValidator.checkValue(self, v):
      if len(v) != 0:
        try:
          float(v)
        except ValueError:
          self.errorMessage = "Please enter an number."
          return False
    
        if self.range != None and (float(v) < min(self.range[0], self.range[1]) or max(self.range[0], self.range[1]) < float(v)):
          self.errorMessage = "%f not in range (%f, %f)" %(float(v), self.range[0], self.range[1])
          return False        
      return True    
    return False
  
class IntegerValidator (NumberValidator):
  def __init__(self, range = None, canEmpty = True):
    NumberValidator.__init__(self, range, canEmpty)
    self.range = range
    
  def Clone(self):
    return IntegerValidator(self.range, self.canEmpty)
  
  def checkValue(self, v):
    if NumberValidator.checkValue(self, v):
      if len(v) != 0:
        try:
          int(v)
        except ValueError:
          self.errorMessage = "Please enter an integer."
          return False
      return True
    return False
