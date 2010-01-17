#!/bin/bash    
# von dan

if [ ! -e "Diagramme" ];
then
  mkdir Diagramme
fi

for file in *.dat
do
  filename=$file
  echo Trying to plot $file ...
  extension=${filename##*.}
  name=${filename%.*}
  title=$(grep Title: ${filename} | sed 's|.*Title:\(.*\)|\1|g') 
  m4 -DNAME=${name} -DFILE=${file} -DTITLE="${title}" multiplot.gpi | gnuplot
done 
