#!/usr/bin/python -tt
import sys
import subprocess
import platform

tmp_name_file = 'tmp_ls_listing.txt'


def RunningOnMac(startDir):
    f_tmp = open(tmp_name_file, 'w')
    subprocess.call(['ls', '-lRS', startDir], stdout=f_tmp)
    f_tmp.close()

    maxFile = 'n/a'
    maxSizeFound = -1
    maxSizeStr = ''
    maxFilePath = ''
    weAreLookingForFirstLine = True
    with open(tmp_name_file, 'r') as f:
        line = f.readline()
        # Here you are in inside the starting directoty,
        # use the while for the recursion only
        # so you get the first line path and the second line total files
        #
        # Skip the first line (total line)
        line = f.readline()
        # Get the second and only interested line here (since ordered by size)
        # manage here the case of empty dir (to do)
        line = f.readline()
        lineElements = line.split()
        if len(lineElements) > 4:
                sVal = lineElements[4]
                if sVal.isdigit():
                    maxSizeFound = long(sVal)
                    maxSizeStr = sVal
                    maxFile = startDir + '/' + lineElements[8]
        # Let's process the recursive values:
        line = f.readline()
        while line:
            if line.startswith('/'):
                maxFilePath = line.rstrip(':\n')
                #print '>>Reading directory ' + maxFilePath
                weAreLookingForFirstLine = True
            else:
                if weAreLookingForFirstLine:
                    lineElements = line.split()
                    if len(lineElements) > 4:
                        weAreLookingForFirstLine = False
                        sVal = lineElements[4]
                        if sVal.isdigit():
                            if (long(sVal) > maxSizeFound):
                                #print 'Found new max ' + sVal
                                #print maxFilePath
                                maxSizeFound = long(sVal)
                                maxSizeStr = sVal
                                maxFile = maxFilePath + '/' + ' '.join(lineElements[8:])
            line = f.readline()
    print '## Biggest file: ' + maxFile
    print '## Size (bytes):  ' + maxSizeStr


def RunningOnLinux(startDir):
    print 'Not implemented for this OS'


def main():
    # Set parameters to run
    if len(sys.argv) != 3:
        print 'Missing one of the two arguments'
        print 'find_biggest_files <directory> <how_many>'
        sys.exit()
    else:
        startDir = sys.argv[1]
        howMany = sys.argv[2]

    #Detect which operative system you are running Python
    os_name = platform.system()
    if os_name.lower() == 'darwin':
        print 'Running Mac'
        RunningOnMac(startDir)
    else:
        print 'Not implemented yet for this operative system'

# boiler plate for linking the main
if __name__ == '__main__':
    main()
