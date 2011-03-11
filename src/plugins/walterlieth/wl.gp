## configuration
set output "{{OUTPUT}}"
set term png size 600,800

# Background
set object 1 rectangle from graph 0,0 to graph 1,1 behind fc rgbcolor "#EEEEff" fs solid noborder

###############
# Plot
###############

set xrange [ 0.5 : 12.5 ]
set lmargin 10
set rmargin 10

set multiplot

# general PRCP
set style fill solid 
set boxwidth 0.5

#######################
##
## PRCP below 100 mm 
## Temp
##
#######################
set key below

set size 1, 0.7
set tmargin 0

set origin 0,0
set border 11
show border 

# x
set xlabel "Monat"
set xtics nomirror
set xtics ("J" 1, "F" 2, "M" 3, "A" 4, "M" 5, "J" 6, "J" 7, "A" 8, "S" 9, "O" 10, "N" 11, "D" 12)

# y - Temp
set ylabel "Temperatur [°C]" #tc rgbcolor "#FF0000" font "Arial,18"
set yrange [0:50]
set ytics 0, 10, 50 tc rgbcolor "#000000"
set grid ytics
set format "  %g"

# y - PRCP
set y2label "Niederschlag [mm]" #tc rgbcolor "#006600"
set y2range [ 0 : 100 ]
set y2tics 0, 20, 100 tc rgbcolor "#000000"
set y2tics nomirror

# first plot
plot \
"{{DATA}}" u 1:5 with boxes axes x1y2 lc rgbcolor "#bbbbff" title "Niederschlag"\
,"{{DATA}}" u 1:2 with lines lc -1 lw 1.5 title "mittl. Temperatur"\
,"{{DATA}}" u 1:3 with lines lc 3 lw 1.5 title "max. Temperatur"\
,"{{DATA}}" u 1:4 with lines lc 1 lw 1.5 title "min. Temperatur"


#######################
##
## above 100 mm PRCP
##
#######################
set title "{{TITLE}}"

# resets
unset key
unset xtics
unset ytics
unset xlabel
unset ylabel
unset y2label
unset yrange

set size 1,0.3
set origin 0.0,0.7
set bmargin 0
set tmargin 5

unset grid
set border 14 
show border

set y2range [ 100 : 300 ]
set y2tics 200, 100, 300
set grid y2tics

# first plot
plot "{{DATA}}" using 1:5 with boxes axes x1y2 lc rgbcolor "#9999ff" title "Niederschlag" 

set nomultiplot
exit
