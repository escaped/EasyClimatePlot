import os
from collections import defaultdict

class Dict(defaultdict):
    def __init__(self, args = None):
        defaultdict.__init__(self, Dict)

    def __repr__(self):
        return dict.__repr__(self)
    
# http://code.activestate.com/recipes/82465/
# TODO licensing. is it allowed to use this code _as is_ ?
def _mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)
