# -*- coding: utf-8 -*-

import Gnuplot
import os

class Contour:
  col1 = []
  col2 = []
  col3 = []

  def __init__ (self, col1, col2, col3):
    pass
  def process (self):
    g = Gnuplot.Gnuplot (persist=1)
    # einfacher contourplot
    # enhanced ermoeglicht erweiterte textdarstellung
    g ('set terminal png size 1024,786 enhanced')
    g ('set output "a_plotted_contour.png"')

    g ('set contour')
    g ('set dgrid3d')

    g ('set title "Lenkoran"')

    # wieviele linien fuer die projektion:
    g ('set cntrparam levels 10')

    # wohin mit der legende
    #set key outside right bottom

    g ('set xtics 1')
    g ('set ytics 2')

    g ('set xtics nomirror')
    g ('set ytics nomirror')

    # z tics sollten nicht sichtbar sein
    g ('unset ztics')

    # monat, mittl. temperatur und mittl. niederschlg.

    g ('set contour base')
    g ('set view 0,0')
    g ('unset surface')

    # create plotitem
    data = Gnuplot.PlotItems.Data (zip (self.col1, self.col2, self.col3), with_ = 'lines')
    g.splot (data)

  def getUserInput (self):
    raise NotImplemented
