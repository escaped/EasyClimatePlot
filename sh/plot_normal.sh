#!/bin/bash    
# von dan

OUTPUTPATH="Diagramme"

if [ ! -e $OUTPUTPATH ];
then
  mkdir $OUTPUTPATH
fi

filename=$1
echo Trying to plot $filename ...
extension=${filename##*.}
name=$(basename ${filename%.*})
title=$(grep Title: ${filename} | sed 's|.*Title:\(.*\)|\1|g') 
m4 -DNAME=${name} -DFILE=${filename} -DTITLE="${title}" -DOUTPUTPATH=${OUTPUTPATH} gnuplot/multiplot.gpi | gnuplot
