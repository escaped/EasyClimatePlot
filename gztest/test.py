import gzip


def test(flags):
  print 'Test %s:' %(flags)
  try:
    f = gzip.open('789820-99999-2004.op.gz', flags)
    f.readlines()[1:] # ignore first line
    f.close()
    print '  success'
  except Exception as e:
    print '  failed: %s' %(e)
    
    
    
test('r')
test('r+')
test('rb')
test('rb+')
test('rU')
test('rU+')
test('rbU')
test('rbU+')
