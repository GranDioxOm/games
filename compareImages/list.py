import os, Image
import config

############# CONSTANTS ###############
FORMATS = ('png', 'jpg')
DIRECTORY = config.DIRECTORYTO
OUTPUTFILE = config.TMPOUTPUTFILE


############# FUNCTIONS ###############

def write_data(file, size):

  output = '{"f":"' + file + '", "w":' + str(size[0]) + ', "h":' + str(size[1]) + "}\n"
  outfile.write(output)

################## RUN ################
outfile = open(OUTPUTFILE, 'w')


for base, dirs, files in os.walk(DIRECTORY):
  for file in files:
    for form in FORMATS:
      filename, file_extension = os.path.splitext(file)
      if form in file_extension:
        imgstr = base + '/' + file
        img = Image.open(imgstr)
        write_data(imgstr, img.size)
        print "Size:"+str(img.size)+" File:"+imgstr
        img.close()

  
outfile.close()
