#!/bin/bash    
# von dan

OUTPUTPATH="Diagramme"

if [ ! -e $OUTPUTPATH ];
then
  mkdir $OUTPUTPATH
fi

filename=$1

case $2 in
  png) FORMAT="png" ; EXTENSION="png" ;;
  eps) FORMAT="postscript eps enhanced"; EXTENSION="eps" ;;
  *)   FORMAT="png" ;;
esac

echo Trying to plot $filename ...
extension=${filename##*.}
name=$(basename ${filename%.*})
title=$(grep Title: ${filename} | sed 's|.*Title:\(.*\)|\1|g') 
m4 -DNAME=${name} -DFILE=${filename} \
-DTITLE="${title}" -DOUTPUTPATH=${OUTPUTPATH} \
-DFORMAT="${FORMAT}" -DEXTENSION="${EXTENSION}" gnuplot/multiplot.gpi | gnuplot
