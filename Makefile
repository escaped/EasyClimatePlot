# Create all sorts of Diagrams using gnuplot
#
.PHONY: clean depend

vpath %.dat data
vpath %.eps Diagramme
vpath %.pdf Diagramme

%.eps: %.dat
	sh/plot_normal.sh $? eps

%.pdf: %.eps
	epstopdf $?

%.png: %.dat
	sh/plot_normal.sh $? png

clean: 
	-rm Diagramme/*
