import io,random, string, sys, os

def createReadDelete(path, length, loop):
   filename = randomword(length)
   fullpath = path + filename
   try:
      with io.open(fullpath, 'w') as f:
        for x in range(10000):
          f.write(u'bingo---------------------------------------------\n'+str(x))

      fd = os.open(fullpath, os.O_RDONLY | os.O_DIRECT)
      for i in xrange(loop):
          print(os.read(fd, 1000000))
   except Exception as e:
      print("Error:")
      print(e)
   finally:
      os.unlink(fullpath)

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def main():
    for arg in sys.argv:
        print arg
    if len(sys.argv) == 5 :
        totalloop = int(sys.argv[4])
        for i in xrange(totalloop):
             createReadDelete(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        print "parameter is path: directory to generate files, length: file name length, loop: how many loop to read before delete, totalLoop: how many times to loop create read delete "

if __name__ == "__main__":
    main()