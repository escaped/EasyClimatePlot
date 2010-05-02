set term png size 400, 500
set title "{{TITLE}}"
set output "{{OUTPUT}}"
 
set tics scale 0
set ytics #tc rgbcolor "#FF0000"
set y2tics 0,20,160 #tc rgbcolor "#006600"
set grid ytics
 
set xrange [0.5:12.5]
set yrange [0:80]
set y2range [0:160]
 
set ylabel "Temperatur (°C)" #tc rgbcolor "#FF0000" font "Arial,18"
set y2label "Niederschlag (mm)" #tc rgbcolor "#006600"
 
set style fill solid #border -1
set boxwidth 0.6
 
set key below 
 
set object 1 rectangle from graph 0,0 to graph 1,1 behind fc rgbcolor "#EEEEff" lw 0
plot "{{DATA}}" using 1:6 with boxes axes x1y2 lc rgbcolor "#bbbbff" title "mittl. Niederschlag" , "{{DATA}}" using 1:3:xtic(2) with lines lc -1 lw 1.5 title "mittl. Temperatur" , "{{DATA}}" using 1:4 with lines lc 1 lw 1.5 title "mittl. max. Temperatur", "{{DATA}}" using 1:5 with lines lc 3 lw 1.5 title "mittl. min. Temperatur"
