## configuration
set title "{{TITLE}}"
set output "{{OUTPUT}}"
set term png size 600,800
set style fill solid 
set border 11
set boxwidth 0.5
set object 1 rectangle from graph 0,0 to graph 1,1 behind fc rgbcolor "#EEEEff" lw 0

###############
# Plot
###############

set multiplot

#######################
##
## above 100 mm PRCP
##
#######################

set xrange [ 0.5 : 12.5 ]
set y2range [ 100 : 300 ]
unset xtics
set y2tics 100,100,300

# we don't want any ytics .. XXX hack
set ytics 100,1000,200 tc rgbcolor "#ffffff"

set size 1,0.3
set origin 0,0.6748
set y2label " "
set ylabel " "
set grid y2tics
unset key

# first plot
plot "{{DATA}}" using 1:5 with boxes axes x1y2 lc rgbcolor "#9999ff" title "Niederschlag" 
unset grid

#######################
##
## below 100 mm PRCP
##
#######################
unset title
set key below

set size 1,0.7

set ytics 0,10, 60 tc rgbcolor "#000000"
set grid ytics
set format "  %g"
set origin 0,0
set yrange [0:49]
set xtics nomirror
set xtics ("J" 1, "F" 2, "M" 3, "A" 4, "M" 5, "J" 6, "J" 7, "A" 8, "S" 9, "O" 10, "N" 11, "D" 12)

set y2tics 0,20,100 tc rgbcolor "#000000"
set y2range [ 0 : 98 ]
set y2tics nomirror

set xlabel "Monat"
set ylabel "Temperatur [°C]" #tc rgbcolor "#FF0000" font "Arial,18"
set y2label "Niederschlag [mm]" #tc rgbcolor "#006600"

# second plot
plot "{{DATA}}" u 1:5 with boxes axes x1y2 lc rgbcolor "#bbbbff" title "Niederschlag",\
"{{DATA}}" u 1:2 with lines lc -1 lw 1.5 title "mittl. Temperatur",\
"{{DATA}}" u 1:3 with lines lc 1 lw 1.5 title "max. Temperatur",\
"{{DATA}}" u 1:4 with lines lc 3 lw 1.5 title "min. Temperatur"

set nomultiplot
exit