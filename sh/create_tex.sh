#!/bin/bash
#
# create_tex.sh:
# Parameters:
#  $1: file that should be included (e. g. example.pdf)
#  $2: data file
#  $3: output file
#

FILE=$1
DATAFILE=$2
OUTPUT=$3

MEANTEMP=$(sh/col_mean.sh $DATAFILE 3)
PRCPSUM=$(sh/col_sum.sh $DATAFILE 2)

cat > Tex_Output/$OUTPUT << _EOF
\includegraphics[scale=0.8]{$FILE}
\\begin{block}
  \\tiny
  \\centering
  \\begin{tabular}{|c|c|}
    \\hline
    \\o Monatstemperatur [C$^\circ$]& $MEANTEMP  \\\\
    \\hline
    $\\Sigma$ Niederschlag [mm] & $PRCPSUM \\\\
    \\hline
  \\end{tabular}
\\end{block}
_EOF
 
