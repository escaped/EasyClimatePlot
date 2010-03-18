# -*- coding: utf-8 -*-

import wx

def ShowMainWindow ():
  app = wx.App (False)
  mw  = MainWindow ()
  app.MainLoop ()

class MainWindow (wx.Frame):
  def __init__ (self):
    wx.Frame.__init__(self, None, title='Klimadaten')


    ######
    # menu bar
    ######
    menuBar = wx.MenuBar ()

    # menus
    programMenu = wx.Menu ()
    menuClose = programMenu.Append (wx.ID_CLOSE, "&Schließen", " Programm schließen")

    helpMenu = wx.Menu ()
    menuAbout = helpMenu.Append (wx.ID_ABOUT, "&About", " Über dieses Programm")

    # append menus to menubar
    menuBar.Append (programMenu, "&Programm")
    menuBar.Append (helpMenu, "&Hilfe")

    # callbacks
    self.Bind (wx.EVT_MENU, self.onClose, menuClose)

    self.Bind (wx.EVT_MENU, self.onAbout, menuAbout)

    # finish menubar construction
    self.SetMenuBar (menuBar)
    
    self.notebook = wx.Notebook (self)
    # das hinzufügen sollte dynamisch vollzogen werden

    import panel
    workflow = panel.Workflow (self.notebook)
    self.notebook.AddPage (workflow, "Download")
    workflow.Create ()
    self.notebook.AddPage (MainPanel (self.notebook), "Plot")
    self.notebook.AddPage (MainPanel (self.notebook), "Export")

    self.Show ()

  def onClose (self, e):
    '''Close the frame'''
    self.Close (True)

  def onAbout (self, e):
    '''Show the about message box'''
    # TODO hier sollte etwas sinnvolles stehen
    mbox = wx.MessageDialog (self, "Ein einfaches Programm.", "Über das Progamm.", wx.OK)
    mbox.ShowModal ()
    mbox.Destroy ()

class MainPanel (wx.Panel):
  def __init__ (self, parent):
    wx.Panel.__init__ (self, parent)
