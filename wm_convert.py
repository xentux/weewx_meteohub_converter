#!/usr/bin/env python
#
#    Copyright (c) 2020 Andre Rupprich <andre@xentux.de>
#
#    See the file LICENSE.txt for your rights.
#
""" Executable that converts meteohub data to CSV. """

from optparse import OptionParser
from weewx_meteohub.importer import Importer

description = """Convert raw data from a meteohub server to a CSV file."""
usage = """usage: %prog [options] arg1 arg2"""


def main():
    # Create a command line parser
    parser = OptionParser(description=description, usage=usage)

    # Add the various options:
    parser.add_option(
        "-i",
        "--input",
        dest="input_file",
        type="string",
        metavar="INPUT_FILE",
        help="Use input file INPUT_FILE.",
    )
    parser.add_option(
        "-o",
        "--output",
        dest="output_file",
        type="string",
        metavar="OUTPUT_FILE",
        help="Use output file OUTPUT_FILE.",
    )

    # Now we are ready to parse the command line:
    options, args = parser.parse_args()

    if not options.input_file:
        print("Missing input file!")
        exit(1)
    if not options.output_file:
        print("Missing output file!")
        exit(1)

    importer = Importer(options.input_file, options.output_file)
    importer.read()


if __name__ == "__main__":
    main()
