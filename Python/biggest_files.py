#!/usr/bin/python -tt
import sys
import os
import subprocess
import platform
import datetime

temporary_file = 'tmp_listing.txt'

class ResultsContainer:
    """
        Result container
    """

    def __init__(self, max_val=1):
        self.max_val = max_val
        self.results = {}
        self.smallest_file = ""

    def update(self, fullpath_filename, file_size):
        """
            Manage the results by adding and removing files depending on the parameters provided.

            fullpath_filename = full path name of the file
            file_size = file size in bytes
        """

        count_files_saved = len(self.results)

        # If it's the first file just add it
        if count_files_saved == 0:
            self.smallest_file = fullpath_filename
            self.results.update({fullpath_filename: file_size})
        else:
            # There is still space in the results to save the file
            if count_files_saved < self.max_val:
                self.results.update({fullpath_filename: file_size})
                if file_size < self.results.get(self.smallest_file, 0):
                    self.smallest_file = fullpath_filename
            else:
                # We reached the maximum number of files collected
                # If file is bigger than the smallest then make space for it and
                # evaluate again the smallest file
                if file_size > self.results.get(self.smallest_file):
                    self.results.pop(self.smallest_file)
                    self.results.update({fullpath_filename: file_size})
                    self.smallest_file = fullpath_filename
                    #Update the smallest file key
                    for key in self.results.keys():
                        if self.results[key] < self.results.get(self.smallest_file):
                            self.smallest_file = key

    def show(self):
        print "### Results ###"
        for key in self.results.keys():
            print 'File %s, size %d' % (key, self.results[key])
        print "### ----- ###"


def RunningOnMac(starting_directory, max_files):
    file_object = open(temporary_file, 'w')
    subprocess.call(['ls', '-lRS', starting_directory], stdout=file_object)
    file_object.close()

    current_size = -1
    current_path = ''
    results = ResultsContainer(max_files)

    with open(temporary_file, 'r') as f:
        #
        """
            Here you are in inside the starting directory, use the while only for the recurisve listing
            where the first line is the path and the second line is total files count.

            Example of output for the current directory:
            total 168
            -rw-r--r--  1 Gianluca  staff  81128 Oct  8 18:08 tmp_ls_listing.txt

        """
        current_path = starting_directory
        # consume the first line which means nothing (total 123)
        line = f.readline()
        # start reading meaningful lines
        line = f.readline()
        while line:
            # If it's a subdirectory update the current path
            if line.startswith('/') or line.startswith('./'):
                current_path = line.rstrip(':\n')
                # Consule the extra line (total 123)
                line = f.readline()
            else:
                    # We are over the lines of directory and total number of lines
                    line_elements = line.split()
                    # I want to process only files
                    if len(line_elements) > 4 and line_elements[0].startswith('-'):
                        size = line_elements[4]
                        if size.isdigit():
                            current_size = int(size)
                            current_file = current_path + '/' + ' '.join(line_elements[8:])
                            results.update(current_file, current_size)
            line = f.readline()
    results.show()
    os.remove(temporary_file)


def RunningOnLinux(starting_directory):
    print 'Not implemented for this OS'


def main():
    # Set parameters to run
    if len(sys.argv) != 3:
        print 'Missing one of the two arguments'
        print 'find_biggest_files <directory> <how_many>'
        sys.exit()
    else:
        starting_directory = sys.argv[1]
        how_many = int(sys.argv[2])

    #Detect which operative system you are running Python
    os_name = platform.system()
    start_time = datetime.datetime.utcnow()
    if os_name.lower() == 'darwin':
        RunningOnMac(starting_directory, how_many)
    else:
        print 'Not implemented yet for this operative system'
    stop_time = datetime.datetime.utcnow()
    print "Execution time {}".format(stop_time-start_time)


# boiler plate for linking the main
if __name__ == '__main__':
    main()
