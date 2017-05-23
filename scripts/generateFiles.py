import io,random, string, sys

def generate(path, length, loop):
   for i in xrange(loop):
      filename = randomword(length)
      with io.open(path + filename, 'w') as f:
         f.write(u'bingo---------------------------------------------'+
             '9999999o--------------------------------------------------')

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def main():
    for arg in sys.argv:
        print arg
    if len(sys.argv) == 4 :
        generate(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        print "parameter is path: directory to generate files, length: file name length, loop: how many files to generate"

if __name__ == "__main__":
    main()