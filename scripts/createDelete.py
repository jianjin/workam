import io,random, string, sys, os

def createDelete(path, length, loop):
   for i in xrange(loop):
      filename = randomword(length)
      fullpath = path + filename
      with io.open(fullpath, 'w') as f:
         f.write(u'bingo---------------------------------------------'+
      	     '9999999o------------------------------------------')

def emptyDirectory(folder):
    for the_file in os.listdir(folder):
       file_path = os.path.join(folder, the_file)
       try:
         if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
       except Exception as e:
         print(e)


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def main():
    for arg in sys.argv:
        print arg
    if len(sys.argv) == 4 :
        createDelete(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        emptyDirectory(sys.argv[1])
    else:
        print "parameter is path: directory to generate files, length: file name length, loop: how many files to generate"

if __name__ == "__main__":
    main()