#-------------------------------------------------------------------------------
# Name:        mcl_graph.py
# Purpose:     CS 8630 Graduate Project, validation part, comparison with other tool
#              this program converts text file into the format, readable by MCL clustering tool
# Author:      Olga
# Created:     22-03-2014
# Copyright:   (c) Olga 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# -------------- simply reads and prints two files -----------------------------

def ReadFiles(afile1, afile2):
    with open(afile1, 'r') as f1, open(afile2, 'r') as f2:
        print f1.read()
        print f2.read()

#-------------------------------------------------------------------------------
# -------------- construct 1 part of the mcl-friendly file  --------------------
def PartOneHeader(afile2):
    f2 = open(afile2, 'w+')
## 'w+' option replaces all with newly overwritten info, will remove the rest - good for starting file from scratch!
    f2.write("(mclheader\nmcltype matrix\ndimensions")
    f2.close()

#-------------------------------------------------------------------------------
# add graph dimension to header's part 1 ---------------------------------------

def AddDimensions (afile1, afile2):
    f2 = open(afile2, 'a')
    k=GraphDimension (afile1)
    #f2.write(' ') # add white space!
    f2.write(' '+str(k)+'x'+str(k)+'\n'+')\n')
    f2.close()

#-------------------------------------------------------------------------------
# build header's optional part 2

def PartTwoHeader(afile1, afile2):
    f2 = open(afile2, 'a')
    f2.write('(mcldoms') ## for renamed nodes in graph! OR  (mcldoms'+' ')
    k=GraphDimension (afile1)

    for x in range(1, k+1): ## by default range is 0 to k
        f2.write(' '+str(x))
    f2.write(' $\n)\n')
    f2.close()

#------------------------------------------------------------------------------
def PartThreeHeader(afile1, afile2):
    f1 = open (afile1, 'r')
    f2 = open(afile2, 'a') ## to append
    lines = f1.readlines()
    f2.write('(mclmatrix\nbegin\n') # actually, part 3

    ## really main code there
    n=0 #keep track of a current node
    d=dict()# empty dictionary!
    counter=1 # don't want to make it =0, just conventionally count nodes from 1 till some n

    for index, line in enumerate(lines): ## for that many lines as number of lines, i.e. "\n"
        line = line.rstrip('\n') ## first, remove '\n' characters
        words = line.split(',') ## divide into words, delimiter is comma
        #print words
        hrenindex = 0
        for idx, word in enumerate(words):
            if idx == 0:
                if word not in d:
                    d[word]=counter
                    counter+=1
                f2.write(str(d[word]) + "   ")
                #print str(d[word]) + "   "
                continue
            if (idx == 1):
                continue;
            if (idx > 1):

                if (idx%2) ==0 :
                    if word not in d:
                        d[word]=counter
                        counter+=1
                    f2.write(str(d[word])+': ')
                    #print str(d[word])+': '
                else:
                    f2.write(word + ' ')
                    #print word + ' '
        f2.write("$\n")

    f2.write(')\n')
    f2.close()

#-------------------------------------------------------------------------------
#----------------  How many nodes are in graph? --------------------------------
## there is no need in this function, as I could have used PartThreeHeader
## but I first have written this one, so I just keep it

def GraphDimension (afile1):
    list_nodes =[]

    f1 = open(afile1, 'r')
    lines = f1.readlines()

    for index, line in enumerate(lines): ## for that many lines as number of "\n"
        line = line.rstrip('\n') # first, remove '\n' characters
        words = line.split(',') # divide into words
        for idx, word in enumerate(words):
                #print idx
                if (idx%2) ==0 : ## because indexes start with 0! be careful!
                    if word not in list_nodes:
                        list_nodes.append(word)

    k = len(list_nodes)
    f1.close()
    return k


#---------- Combine all header's parts together --------------------------

def ConstructConverted(afile1, afile2):
    PartOneHeader(afile2) ## constructs part 1 of the header
    AddDimensions (afile1, afile2) ## adds dimensions to the part 1 of th header
    PartTwoHeader(afile1, afile2) ## adds optional part 2 of the header; convenient when nodes renamed!!!
    PartThreeHeader(afile1, afile2) ## adds part 3 of the header; MAIN LOGIC


#-----------------------------  MAIN  ------------------------------------------

def main():

    ##ReadFiles('one.txt','two.txt') # uncomment to read both input and output files

    # names of the files! change first one "one.txt" to input, second "two.txt" to output name
    ##ConstructConverted('one.txt','two.txt')
    #put the file(s) of interest into the same directory, as this pythin program
    ConstructConverted('100_out_all_raw.txt','100_out_all_raw_converted.txt')
    #ConstructConverted('100_out_raw.txt','100_out_raw_converted.txt')
    ## ~ 6-7 seconds for files with 100 nodes

    ##print ("====================="+'\n')


if __name__ == '__main__':
    main()
