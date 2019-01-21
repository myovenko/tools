#!/usr/bin/python
import sys  
import os
import re

PARAM_TEMPLATE = '\${%s}'
#-------------------------------------------------------------------------------
def main():
   if len(sys.argv) < 3: usage()

   dataset_file = sys.argv[1]
   if not os.path.isfile(dataset_file):
      print("File {} does not exist".format(dataset_file))
      usage()

   template_file = sys.argv[2]
   if not os.path.isfile(template_file):
      print("File {} does not exist".format(template_file))
      usage()
       
   vars_sets = loadDatasets(dataset_file)
   #print("Var sets: {}".format(vars_sets)) #debug

   for var_set in vars_sets:
     runTemplate(template_file, var_set)

#-------------------------------------------------------------------------------
def usage():
   print("USAGE: python template_filler.py <var sets file> <template file>")
   sys.exit()

def loadDatasets(dataset_file):
   header_pos = {}
   vars_sets = []
   with open(dataset_file) as fp:
      cnt = 0
      for line in fp:
        line = line.rstrip('\n')
        if not line.strip(): continue
        if cnt == 0:
          header_pos = parseHeader(line)
          cnt +=1
          continue
        cnt += 1
        vars_sets.append(parseSet(line, header_pos))
   return vars_sets

def parseHeader(line):
   header_pos = {}
   split_line = re.split("[\t ]+", line)
   cnt = 0
   for word in split_line:
      header_pos[cnt] = word
      cnt += 1
   return header_pos

def parseSet(line, header_pos):
  data_set = {}
  split_line = re.split("[\t ]+", line)
  cnt = 0
  for word in split_line:
       data_set[header_pos[cnt]] = word
       cnt += 1
  return data_set

def runTemplate(template_file, var_set):
  result = ''
  with open(template_file) as fp:
    result = fp.read()
    for key, value in var_set.items():
      pattern = PARAM_TEMPLATE % key
      #print('using %s to %s' % (pattern, value)) #debug
      result = re.sub(pattern, value, result)
  print("Result:")
  print(result)

#-------------------------------------------------------------------------------
  
if __name__ == '__main__':  
   main()
