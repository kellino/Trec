#!/usr/bin/python2.7
import subprocess


class FileHandler():
    def find_file(self, search, extension):
        # not very portable solution to finding the files on the system
        filepath = subprocess.check_output(
            'find ~/ -type f -name "{}" | grep -i {}'.format(
                extension, search), shell=True)
        return filepath.strip()

    def close_file(self, filename):
        if filename is not None:
            try:
                filename.close()
            except:
                "unable to close file"
