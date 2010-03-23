.PHONY: clean

todos:
	echo "Trying to find todos.."
	sh ./bin/todos

# make clean..
#
clean:
	for file in $$(find . -name "*.pyc"); do rm $$file; done
	-rm core
