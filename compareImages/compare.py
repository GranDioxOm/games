from itertools import izip
import Image, os
import config, json

############# CONSTANTS ###############
INPUTFILE = config.TMPOUTPUTFILE
#OUTPUTFILE = config.INCLUDEFILES

ERRORFILE = 'compare.err'
DIRECTORY = config.DIRECTORYFROM
FILETRUE = config.FILETRUE
FILEFALSE = config.FILEFALSE


DATAFILES = {}

############# FUNCTIONS ###############

#def write_data(file, size):
#  pass

def log_error(line):
  errorfile.write(line)

def write_true(file1, file2):
  filetrue.write(file1 + " -> " + file2 + "\n")

def write_false(file):
  filefalse.write(file + "\n")
  



def compare(file1, file2):
  i1 = file1
  i2 = file2
  pairs = izip(i1.getdata(), i2.getdata())
  if len(i1.getbands()) == 1:
      # for gray-scale jpegs
      dif = sum(abs(p1-p2) for p1,p2 in pairs)
  else:
      dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
   
  ncomponents = i1.size[0] * i1.size[1] * 3
  difpercent = (dif / 255.0 * 100) / ncomponents

  if difpercent == 0:
    return True
  else:
    return False




################## RUN ################
#open files
infile = open(INPUTFILE, 'r') 
errorfile = open(ERRORFILE, 'w')
filetrue = open(FILETRUE, 'w')
filefalse = open(FILEFALSE, 'w')



# read images data

for line in infile:
  try:
    #print line
    data = json.loads(line)

    if not DATAFILES.has_key(data['w']):
      DATAFILES[data['w']] = {}

    if not DATAFILES[data['w']].has_key(data['h']):
      DATAFILES[data['w']][data['h']] = []
    
    DATAFILES[data['w']][data['h']].append(data['f'] )

  except:
    log_error(line)

infile.close()


#compare images
for base, dirs, files in os.walk(DIRECTORY):
  for file in files:
    file1 = base+'/'+ file
    print file1
    exist = False
    i1 = Image.open(file1)
    if DATAFILES.has_key(i1.size[0]):
      if DATAFILES[i1.size[0]].has_key(i1.size[1]):

        for fcomp in DATAFILES[i1.size[0]][i1.size[1]]:
          i2 = Image.open(fcomp)
          if compare(i1, i2):
            write_true(file1, fcomp)
            exist = True

    if not exist:
      write_false(file)
          

#close files

errorfile.close()
filetrue.close() 
filefalse.close()

