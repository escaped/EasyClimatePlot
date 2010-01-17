# Create all sorts of Diagrams using gnuplot
#
.PHONY: clean depend

vpath %.dat data
vpath %.eps Diagramme

%.eps: %.dat
	sh/plot_normal.sh $?

clean: 
	-rm Diagramme/*
