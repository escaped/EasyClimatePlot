import Gnuplot
import os

class WalterLieth (Gnuplot):
  filename = ""

  def process (self):
    # plot a walther-lieth diagramm
    g = Gnuplot.Gnuplot ()

    # TODO title
    g.title("TITLE")

    ## configuration
    g('set style fill solid') #border -1
    g('set border 11')
    g('set boxwidth 0.5')
    g('set object 1 rectangle from graph 0,0 to graph 1,1 behind fc rgbcolor "#EEEEff" lw 0')

    ###############
    # Plot
    ###############

    set multiplot
    #######################
    ##
    ## above 100 mm PRCP
    ##
    #######################

    g('set xrange [ 0 : 12.5 ]')
    g('set y2range [ 100 : 300 ]')
    g('unset xtics')
    g('set y2tics 100,100,300')

    # we don't want any ytics .. XXX hack
    g('set ytics 100,1000,200 tc rgbcolor "#ffffff"')

    g('set size 1,0.3')
    g('set origin 0,0.616')
    g('set y2label " "')
    g('set ylabel " "')
    g('set grid y2tics')
    g('unset key')

    # TODO first plot
    plot "FILE" using 1:2 with boxes axes x1y2 lc rgbcolor "#bbbbff" title "mittl. Niederschlag"
    g('unset grid')

    #######################
    ##
    ## below 100 mm PRCP
    ##
    #######################
    g('unset title')
    g('set key below')

    g('set size 1,0.7')

    g('set ytics 0,10, 60 tc rgbcolor "#000000"')
    g('set grid ytics')
    g('set format "  %g"')
    g('set origin 0,0')
    g('set yrange [0:60]')
    g('set xtics nomirror')

    g('set y2tics 0,20,100 tc rgbcolor "#000000"')
    g('set y2range [ 0 : 99 ]')
    g('set y2tics nomirror')

    g('set xlabel "Monat"')
    g('set xmtics')
    g('set ylabel "Temperatur (°C)" #tc rgbcolor "#FF0000" font "Arial,18"')
    g('set y2label "Niederschlag (mm)" #tc rgbcolor "#006600"')

    # TODO second plot
    plot "FILE" using 1:2 with boxes axes x1y2 lc rgbcolor "#bbbbff" title "mittl.  Niederschlag",\
         "FILE" using 1:3:xtic(1) with lines lc -1 lw 1.5 title "mittl. Temperatur"
    g('set nomultiplot')

    # TODO save to file

  def getUserInput (self):
    print 'hallo'

