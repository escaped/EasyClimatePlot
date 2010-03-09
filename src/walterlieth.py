import Gnuplot
import os

class WalterLieth (Gnuplot):
  filename = ""

  def process (self):
    # plot a walther-lieth diagramm
    g = Gnuplot.Gnuplot ()

    # TODO title
    g ('set title "TITLE"')

    g ('set tics scale 1')
    g ('set ytics #tc rgbcolor "#FF0000"')
    g ('set y2tics 0,20,100 #tc rgbcolor "#006600"')
    g ('set y2tics 100,100,400')
    g ('set grid ytics')

    g ('set xrange [0.5:12.5]')
    g ('set yrange [0:60]')
    g ('set y2range [0:400]')

    g(set ylabel "Temperatur (°C)"') #tc rgbcolor "#FF0000" font "Arial,18"')
    g(set y2label "Niederschlag (mm)"') #tc rgbcolor "#006600"')

    g('set xlabel "Monat"')

    g('set style fill solid') #border -1
    g('set boxwidth 0.5')

    g('set key below')

    g('set object 1 rectangle from graph 0,0 to graph 1,1 behind fc rgbcolor "#EEEEff" lw 0')

    # data files
    # TODO files
    f = Gnuplot.File (os.path.join (os.getcwd (), filename))

    plot "FILE" using 1:6 with boxes axes x1y2 lc rgbcolor "#bbbbff" title "mittl. Niederschlag" ,\
       "FILE" using 1:2:xtic(1) with lines lc -1 lw 1.5 title "mittl. Temperatur" ,\
       "FILE" using 1:3 with lines lc 1 lw 1.5 title "mittl. max. Temperatur",\
       "FILE" using 1:4 with lines lc 3 lw 1.5 title "mittl. min. Temperatur"

    # save the file
    g.hardcopy ("NAME.ps", enhanced=1, color=1)


  def getUserInput (self):
    print 'hallo'

