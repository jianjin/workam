import io
for i in xrange(1000):
   with io.open("efs/lockunlockclose/"+"file_"+str(i), 'w') as f:
      f.write(u'bingo---------------------------------------------'+
      	'9999999o--------------------------------------------------')