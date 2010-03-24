from mvc.control import Control


class PlotTypeControl (Control):
  def __init__ (self, view):
    Control.__init__ (self, view)

  def onWalterLieth (self, e):
    self.view.parent.switchSubPanelByName ("WalterLiethWizard")

