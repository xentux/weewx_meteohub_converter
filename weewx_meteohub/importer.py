from weewx_meteohub.sensor import Sensor
import datetime
import csv


class Importer:
    """ Class with methods for importing meteohub data to weewx """

    def __init__(self, input_file, output_file):
        # Open input and output files
        try:
            self.input_file = open(input_file, "r")
        except FileNotFoundError:
            return False

        self.output_file = open(output_file, "w")
        fieldnames = [
            "date_time",
            "temp",
            "hum",
            "dew",
            "pressure",
            "baro",
            "wind_dir",
            "gust_speed",
            "wind_speed",
            "wind_chill",
            "rain",
            "rain_rate",
            "rad",
        ]

        # instanciate csv writer
        self.csv_writer = csv.DictWriter(
            self.output_file, fieldnames=fieldnames
        )

        # Write csv header
        self.csv_writer.writeheader()

    def __del__(self):
        # Close input and output files
        self.input_file.close()
        self.output_file.close()

    def count_lines(self):
        """
        Counts the lines in the input file
        This method is not used in the moment and may be deleted in future.
        """
        count = 0
        self.input_file.seek(0, 0)
        for count, line in enumerate(self.input_file, 1):
            pass
        return count

    def get_start_date(self):
        """ Reads the datetime of the first line in our input file """
        self.input_file.seek(0, 0)
        first_line = self.input_file.readline()
        sensor = Sensor(first_line)
        return sensor.get_date()

    def roundto5(self, number):
        """ Rounds the given value down to the next 0 or 5 digit """
        modulo = number % 5
        return number - modulo

    def get_interval(self, date=None):
        """ Returns the 5 minute interval to the given datetime """
        if not date:
            date = self.get_start_date()

        start_minute = self.roundto5(int(date.strftime("%M")))
        interval_start = date.replace(minute=start_minute, second=0)
        interval_end = interval_start + datetime.timedelta(minutes=5)

        return interval_start, interval_end

    def write(self, time, thd, thdb, wind, rain, sol):
        """
        Writes csv data
        Temperatures will be rounded to 1 decimal digit
        Wind direction, solar radiation and humidity will be rounded
        to a integer
        """

        time = time.strftime("%Y-%m-%d %H:%M")
        csv_data = {}
        csv_data["date_time"] = time
        csv_data["temp"] = thd[0]
        csv_data["hum"] = thd[1]
        csv_data["dew"] = thd[2]
        csv_data["pressure"] = thdb[3]
        csv_data["baro"] = thdb[4]
        csv_data["wind_dir"] = wind[0]
        csv_data["gust_speed"] = wind[1]
        csv_data["wind_speed"] = wind[2]
        csv_data["wind_chill"] = wind[3]
        csv_data["rain"] = rain[1]
        csv_data["rain_rate"] = rain[0]
        csv_data["rad"] = sol

        self.csv_writer.writerow(csv_data)

    def read(self):
        """ Reads the input_file and aggregates the 5-minute values """
        start_date = self.get_start_date()
        print(f"Starting import at {start_date} ...")

        file_position = 0
        self.input_file.seek(file_position)

        # Count the number of imported data sets
        datasets_imported = 0

        # Initialize data
        thd_value_list = []
        thdb_value_list = []
        wind_value_list = []
        rain_value_list = []
        sol_value_list = []

        interval_start, interval_end = self.get_interval(start_date)
        print(f"First interval: {interval_start} - {interval_end}")

        for datasets_total, line in enumerate(self.input_file, 1):
            sensor_data = Sensor(line)
            if interval_start <= sensor_data.get_date() < interval_end:
                # print(f"in range - {sensor_data.get_date()}")
                # print(f"{datasets_total}: {line}")
                file_position += len(line)

                if sensor_data.get_sensor_name() == "th0":
                    thd_value_list.append(sensor_data.get_th_values())
                    datasets_imported += 1
                elif sensor_data.get_sensor_name() == "thb0":
                    thdb_value_list.append(sensor_data.get_thb_values())
                    datasets_imported += 1
                elif sensor_data.get_sensor_name() == "wind0":
                    wind_value_list.append(sensor_data.get_wind_values())
                    datasets_imported += 1
                elif sensor_data.get_sensor_name() == "rain0":
                    rain_value_list.append(sensor_data.get_rain_values())
                    datasets_imported += 1
                elif sensor_data.get_sensor_name() == "sol0":
                    sol_value_list.append(sensor_data.get_sol_value())
                    datasets_imported += 1
                elif sensor_data.get_sensor_name() == "uv0":
                    pass
            else:
                print(f"Time: {interval_end}\r", end="")
                # print(f"---------- Time: {interval_end}-------------")

                rate, total = sensor_data.get_rain_mean_values(rain_value_list)

                self.write(
                    interval_end,
                    sensor_data.get_th_mean_values(thd_value_list),
                    sensor_data.get_thb_mean_values(thdb_value_list),
                    sensor_data.get_wind_mean_values(wind_value_list),
                    sensor_data.get_rain_mean_values(rain_value_list),
                    sensor_data.get_sol_mean_value(sol_value_list),
                )

                # next interval
                if self.get_interval(sensor_data.get_date()):
                    interval_start = interval_end
                    interval_end = interval_start + datetime.timedelta(
                        minutes=5
                    )

                # one line back (we have to read the last dataset again)
                self.input_file.seek(file_position)

                # Delete last interval data
                thd_value_list = []
                thdb_value_list = []
                wind_value_list = []
                rain_value_list = []
                sol_value_list = []

        # write last interval
        self.write(
            interval_end,
            sensor_data.get_th_mean_values(thd_value_list),
            sensor_data.get_thb_mean_values(thdb_value_list),
            sensor_data.get_wind_mean_values(wind_value_list),
            sensor_data.get_rain_mean_values(rain_value_list),
            sensor_data.get_sol_mean_value(sol_value_list),
        )

        # Show some information
        print(f"Finished import at {interval_end}")
        print(f"{datasets_imported} of {datasets_total} datasets imported.")
