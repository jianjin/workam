import io,random, string, sys, os, uuid

def generate(path, length, loop):
   print "Generating files in " + path
   for i in xrange(loop):
      filename = randomword(length)
      with io.open(path + filename, 'w') as f:
         f.write(u'bingo---------------------------------------------'+
             '9999999o--------------------------------------------------')

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def removeAll(path):
    print "Remving all files in " + path
    for the_file in os.listdir(path):
       file_path = os.path.join(path, the_file)
       try:
          os.unlink(file_path)
       except Exception as e:
          print(e)

def main():
    for arg in sys.argv:
        print arg
    if len(sys.argv) == 5 :
        for i in xrange(int(sys.argv[4])):
           print "round " + str(i)
           path = sys.argv[1] + str(uuid.uuid4()) + "/"
           os.makedirs(path)
           generate(path, int(sys.argv[2]), int(sys.argv[3]))
           removeAll(path)
           os.listdir(path)
    else:
        print "parameter is path: directory to generate files, length: file name length, loop: how many files to generate, round: how many round to generate and clean"

if __name__ == "__main__":
    main()