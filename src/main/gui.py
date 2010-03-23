# -*- coding: utf-8 -*-

import wx
import main.splashscreen

from main.pluginselection import PluginSelection
from plot.gui import PlotIntro
from export.gui import ExportIntro

def ShowMainWindow ():
  app = wx.App (False)
  splash = main.splashscreen.Splashy ()
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

    # TODO anders machen
    #workflow = NOAA_Wizard (self.notebook)
    #self.notebook.AddPage (workflow, "Download")
    #workflow.initSubPanel ()

    selection = PluginSelection(self.notebook)
    self.notebook.AddPage (selection, "Download")
    
    plot = PlotIntro (self.notebook)
    self.notebook.AddPage (plot , "Plot")
    plot.initSubPanel ()

    self.notebook.AddPage (ExportIntro (self.notebook), "Export")
    self.notebook.AddPage (EmptyPanel (self.notebook), "Daten verwalten")

    self.Layout()
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

class EmptyPanel (wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)

