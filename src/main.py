#!/usr/bin/python

import sys

from control.control import Control
import gui.window

gui.window.ShowMainWindow ()
exit ()

def dowhile (text, condition):
  choose = 0
  print text
  while True:
    print ":-> ",
    choose = sys.stdin.readline()[0]
    if choose in condition: break

    print '''
    please choose according to the list.'''
  return choose
def main ():
  # choose task
  choose = dowhile ('''Please choose task:
      1) Download Data
      2) Process Data''', ['1','2'])

  # choose plugin
  if choose == '1':
    chooseplugin = dowhile ('''Please choose plugin:
    1) NOAA
    2) NASA''',['1','2'])

    plugin = 0
    if chooseplugin == '1':
      # noaa
      import noaa
      plugin = noaa.NOAA ()
    elif chooseplugin == '2':
      # nasa
      import nasa
      plugin = nasa.NASA ()

    print "===================== %s =================" %(plugin.name)
    plugin.getUserInput ()
    plugin.downloadData ()
    data = plugin.getData ()

    choose_processplugin = dowhile ('''Please choose a process plugin:
    1) Map
    2) Contour
    3) Walter-Lieth''', ['1','2','3'])

    output_plugin = 0
    if choose_processplugin == '1':
      pass
    elif choose_processplugin == '2':
      pass
    elif choose_processplugin == '3':
      import walterlieth
      output_plugin = walterlieth.WalterLieth ()

    output_plugin.setDataObjects (data)
    output_plugin.getUserInput ()
    output_plugin.process ()

  elif choose == '2':
    pass

if __name__ == "__main__":
  main ()
