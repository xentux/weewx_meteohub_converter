from datetime import datetime
import statistics
import math


class Sensor:
    def __init__(self, line):
        self.data = line.split(" ")

    def get_date(self):
        """ Returns the date """
        return datetime.strptime(self.data[0], "%Y%m%d%H%M%S")

    def get_sensor_type(self):
        """ Returns the sensor type, f.e. thb. """
        return self.data[1][:-1]

    def get_sensor_number(self):
        """ Returns the sensor number """
        return int(self.data[1][-1])

    def get_sensor_name(self):
        """ Returns the full sensor name, f.e. wind0 """
        return self.data[1]

    def get_t_value(self):
        """ Returns the value of a t sensor """
        return float(self.data[2]) / 10

    def get_t_mean_value(self, value_list):
        """ Returns the mean values of a given t-value list """
        if not len(value_list):
            return None
        else:
            return round(statistics.mean(value_list), 1)

    def get_th_values(self):
        """ Returns the values (temp/hum) of a th sensor """
        return (
            float(self.data[2]) / 10,   # tempOut
            int(self.data[3]),          # hum
            float(self.data[4]) / 10,   # Dew
        )

    def get_thb_values(self):
        """
        Returns values (temp/hum/dew/baro/forecast/sealevel) of a thb sensor
        """
        return (
            float(self.data[2]) / 10,  # temp
            int(self.data[3]),  # hum
            float(self.data[4]) / 10,  # dew
            float(self.data[5]) / 10,  # baro QNH
            int(self.data[6]),  # forecast
            float(self.data[7]) / 10,  # pressure at sealevel
        )

    def get_th_mean_values(self, value_list):
        """ Returns the mean values of a given th-value list """
        """ Return also Tmin and Tmax """
        if not len(value_list):
            return None, None, None, None, None
        t, h, d = map(list, zip(*value_list))
        return (
            round(statistics.mean(t), 1),
            int(round(statistics.mean(h), 0)),
            round(statistics.mean(d), 1),
            round(min(t), 1),
            round(max(t), 1),
        )

    def get_thb_mean_values(self, value_list):
        """ Returns the mean values of a given th-value list """
        if not len(value_list):
            return None, None, None, None, None

        temp, hum, dew, baro, forecast, sealevel = map(list, zip(*value_list))
        return (
            round(statistics.mean(temp), 1),
            int(round(statistics.mean(hum), 0)),
            round(statistics.mean(dew), 1),
            round(statistics.mean(baro), 1),
            round(statistics.mean(sealevel), 1),
        )

    def get_wind_values(self):
        """ Returns values (dir/gust/avg/chill) of a wind sensor """
        return (
            int(self.data[2]),  # dir
            float(self.data[3]) / 10,  # gust
            float(self.data[4]) / 10,  # avg
            float(self.data[5]) / 10,  # chill
        )

    def get_wind_mean_values(self, value_list):
        """ Returns the mean values of a given wind-value list """
        if not len(value_list):
            return None, None, None, None

        dir, gust, avg, chill = map(list, zip(*value_list))
        return (
            int(round(statistics.mean(dir), 0)),
            round(statistics.mean(gust), 1),
            round(statistics.mean(avg), 1),
            round(statistics.mean(chill), 1),
        )


    def get_rain_values(self):
        """ Returns the rain sensor values (rate/total) """
        return float(self.data[2]) / 10, float(self.data[4]) / 10

    def get_rain_cumul(self, value_list):
        """ Returns the last values of a rain total sensor """
        if not len(value_list):
            return None

        rate, total = map(list, zip(*value_list))
        rain_cumul = round(total[-1], 1)

        return rain_cumul

    def get_rain_mean_values_consolidate(self, value_list, last_cumul):
        """ Returns the mean values of a rain sensor """
        if not len(value_list):
            return None, None
        #if math.isnan(last_cumul):
        #    return None, None
        rate, total = map(list, zip(*value_list))
        rain = round(((total[-1] - total[0])+(total[0]-last_cumul)), 1)

        # Rain can't be negative and in january many rain sensors are
        # resetted to 0 which leads to negative values
        if rain < 0:
            rain = 0.0
        return round(statistics.mean(rate)), rain

    def get_rain_mean_values(self, value_list):
        """ Returns the mean values of a rain sensor """
        if not len(value_list):
            return None, None

        rate, total = map(list, zip(*value_list))
        rain = round(total[-1] - total[0], 1)

        # Rain can't be negative and in january many rain sensors are
        # resetted to 0 which leads to negative values
        if rain < 0:
            rain = 0.0
        return round(statistics.mean(rate)), rain
