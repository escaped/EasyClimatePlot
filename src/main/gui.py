# -*- coding: utf-8 -*-

import wx
import sys
import main.splashscreen

from main.pluginselection import PluginSelection
from export.gui import ExportIntro

import config

def ShowMainWindow ():
  app = wx.App (False)
  splash = main.splashscreen.Splashy ()
  mw  = MainWindow ()
  mw.Show()
  config.createOutputStreams ()
  app.MainLoop ()

class MainWindow (wx.Frame):
  def __init__ (self):
    wx.Frame.__init__(self, None, title='Klimadaten', size=(600, 400))
    self.SetMinSize(self.GetSize())
       
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
    self.Bind (wx.EVT_CLOSE, self.onClose)

    # finish menubar construction
    self.SetMenuBar (menuBar)
    
    self.notebook = wx.Notebook (self)
    # das hinzufügen sollte dynamisch vollzogen werden

    import pluginmanager
    # TODO eigentlich reicht eine Instanz mit entsprechendem Event auf der TabSelection!!!
    selectionIn = PluginSelection(self.notebook,pluginmanager.WizardPlugin.T_INPUT)
    selectionIn.initSubPanel()    
    
    selectionOut = PluginSelection(self.notebook,pluginmanager.WizardPlugin.T_OUTPUT)
    selectionOut.initSubPanel()    
    
    self.notebook.AddPage (selectionIn, "Input/Download")    
    self.notebook.AddPage (selectionOut , "Output/Plot")

    self.Layout()

  def onClose (self, e):
    '''Stop the program'''
    dlg = wx.MessageDialog(self, 
            "Do you really want to close this application?",
            "Confirm Exit", wx.YES_NO|wx.ICON_QUESTION)
    result = dlg.ShowModal()
    dlg.Destroy()
    if result == wx.ID_YES:
      sys.exit()

  def onAbout (self, e):
    '''Show the about message box'''
    # TODO hier sollte etwas sinnvolles stehen
    mbox = wx.MessageDialog (self, "Ein einfaches Programm.", "Über das Progamm.", wx.OK)
    mbox.ShowModal ()
    mbox.Destroy ()

class EmptyPanel (wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)

