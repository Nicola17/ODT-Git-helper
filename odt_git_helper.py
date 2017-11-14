from __future__ import print_function

import os
import zipfile
import argparse
import xml.dom.minidom

def createODT(path, zipName, args):
    compression_mode = zipfile.ZIP_DEFLATED if args.zlib else zipfile.ZIP_STORED
    zipf = zipfile.ZipFile(zipName, 'w', compression_mode)
    for root, dirs, files in os.walk(path):
        for file in files:
            if 'Thumbs.db' in file:
                continue
            zipf.write(os.path.join(root, file), os.path.join(root, file)[path.__len__():])
            if args.verbose:
                print(os.path.join(root, file)[path.__len__():])

        for dir in dirs:
            zipf.write(os.path.join(root, dir), os.path.join(root, dir)[path.__len__():])
            if args.verbose:
                print(os.path.join(root, dir)[path.__len__():])

    zipf.close()

def extractODT(path, zipName, args):
    zipf = zipfile.ZipFile(zipName,'r')
    for name in zipf.namelist():
        zipf.extract(name, path)
    zipf.close()

    if args.verbose:
        print("Pretty xml generation")
    for root, dirs, files in os.walk(path):
        for file in files:
            fileWPath = os.path.join(root, file)
            if fileWPath[-3:] == "xml":
                if args.verbose:
                    print(fileWPath)

                statinfo = os.stat(fileWPath)
                if statinfo.st_size == 0:
                    continue

                xmlFile = xml.dom.minidom.parse(fileWPath)
                pretty_xml_as_string = xmlFile.toprettyxml()

                out_file = open(fileWPath,"wb")
                out_file.write(pretty_xml_as_string.encode('utf-8'))
                out_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract/Create an odt file in/from a directory.')

    parser.add_argument("-v","--verbose", action='store_true', default=False, help="increase output verbosity")
    parser.add_argument("-z","--zlib", action='store_true', default=False, help="use deflated compression")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--compress", action="store_true", default=False, help='compress into an .odt file')
    group.add_argument("-e", "--extract", action="store_true", default=False, help='extract odt file into a directory (default)')

    parser.add_argument('directory', metavar='Directory', type=str, help='target/destination directory')
    parser.add_argument('odt_file', metavar='ODT_File', type=str, help='target/destination odt file')

    args = parser.parse_args()

    if args.zlib and args.extract:
        print 'Note: zlib compression is only used when compressing the files'

    if args.extract or (not args.extract and not args.compress):
        print('Extract files')
        extractODT(args.directory, args.odt_file, args)

    if args.compress:
        print('Compress files')
        createODT(args.directory, args.odt_file, args)