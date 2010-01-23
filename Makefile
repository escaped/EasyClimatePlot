# Create all sorts of Diagrams using gnuplot
#
.PHONY: clean depend

vpath %.dat data
vpath %.eps Diagramme
vpath %.pdf Diagramme
vpath %.tex Tex_Output

%.eps: %.dat
	sh/plot_normal.sh $? eps

%.pdf: %.eps
	epstopdf $?

%.png: %.dat
	sh/plot_normal.sh $? png

%.tex: %.pdf %.dat
	sh/create_tex.sh $^ $@

clean: 
	-rm Diagramme/*
