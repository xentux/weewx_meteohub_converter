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

Then use *wee_import* to impor the csv file to WeeWX, f.e. `wee_import --import-config=config/csv.conf`

I provided an example config file in */config*.

## Todo
At the moment the converter only works for a single raw data file. It should convert a provided path with all raw data from a meteohub server.