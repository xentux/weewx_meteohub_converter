# WeeWX meteohub raw data converter
A converter for [meteohoub](https://wiki.meteohub.de/Main_Page) raw data.
It converts meteohub raw data to csv, which is importable by **WeeWX**
## Development
This is a very, very first commit of my [WeeWX](http://www.weewx.com) meteohub importer.
At this point of development, the importer works for me, but there is really **a lot to do** to make it usable for everyone!

If you have need to import meteohub raw data to your WeeWX system or want to contribute, don't hesitate to contact me. I'll try to help.

## Usage
This python module reads the meteohub raw data and converts it to csv files which can be imported to WeeWX using the WeeWX wee_import util.

`./wm_convert.py -i 202001/raw -o 202001.csv`

Then use *wee_import* to import the csv file to WeeWX, f.e. `wee_import --import-config=config/csv.conf`

I provided an example config file in */config*.

## How does it work?
The converter reads the given raw data file, sorts the datasets (lines) by date and writes this sorted data to a temporary file. (I don't want to touch the original data - just for the case that someone doesn't have a backup.) I discovered the issue that the meteohub raw data files may not be in chronological order. This causes issues during calcuating the time condensed input data. That's the cause why I sort the input data.
The converter reads now the data for 5 minute intervals and calculates the mean values for temperatures, humidity and wind. Rain will be summed up for that interval.
At the end the intervals are written to the output file in CSV format. You can import now this data to WeeWX. At the moment it makes sense, to look over the output file - you may open it in Excel or Numbers f.e. - and do a visual inspection.

## Todo
- Adding min/max values to mean data functions
- Support for sensors with leading 0 in the value string
- Adding support for importing a complete raw data path
- Implement T-sensors

## History
- Added input file sorting 
