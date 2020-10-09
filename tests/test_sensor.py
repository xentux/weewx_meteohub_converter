from weewx_meteohub.sensor import Sensor
from datetime import datetime


t_data = "20071101145906 t0 132"
th_data = "20071101145906 th0 132 82 10"
thb_data = "20071101145830 thb0 218 46 10 10240 3 10240"
wind_data = "20110916104500 wind0 69 4 4 0189"
sol_data = "20110916104143 sol0 487 30"
rain_data = "20110909152323 rain0 0 0 8470"
uv_data = "20180601000145 uv0 0"


def test_get_date():
    sensor = Sensor(thb_data)
    assert isinstance(sensor.get_date(), datetime)
    assert sensor.get_date().strftime("%Y%m%d%H%M%S") == "20071101145830"


def test_get_senor_type():
    sensor = Sensor(thb_data)
    assert sensor.get_sensor_type() == "thb"


def test_get_sensor_number():
    sensor = Sensor(thb_data)
    assert isinstance(sensor.get_sensor_number(), int)
    assert sensor.get_sensor_number() == 0


def test_get_sensor_name():
    sensor = Sensor(thb_data)
    assert sensor.get_sensor_name() == "thb0"


def test_get_t_value():
    sensor = Sensor(t_data)
    temp = sensor.get_t_value()
    assert temp == 13.2


def test_get_th_values():
    sensor = Sensor(th_data)
    temp, hum, dew = sensor.get_th_values()
    assert temp == 13.2
    assert hum == 82
    assert dew == 1.0


def test_get_th_mean_values():
    sensor = Sensor(th_data)
    values_list = [(5, 2, 3.1), (8, 2, 3.1), (8.5, 2, 3.5)]
    t, h, d = sensor.get_th_mean_values(values_list)
    assert t == 7.2
    assert h == 2
    assert d == 3.2


def test_get_thb_values():
    sensor = Sensor(thb_data)
    temp, hum, dew, baro, fc, sealevel = sensor.get_thb_values()
    assert temp == 21.8
    assert hum == 46
    assert dew == 1.0
    assert baro == 1024
    assert fc == 3
    assert sealevel == 1024


def test_get_thb_mean_values():
    sensor = Sensor(thb_data)
    values_list = [
        (5.1, 25, -3, 1024.0, 1, 1024.0),
        (5.3, 26, -3.3, 1024.3, 1, 1024.3),
        (5.5, 28, -3.4, 1024.8, 1, 1025),
    ]
    t, h, d, b, sl = sensor.get_thb_mean_values(values_list)
    assert t == 5.3
    assert h == 26
    assert d == -3.2
    assert b == 1024.4
    assert sl == 1024.4


def test_get_wind_values():
    sensor = Sensor(wind_data)
    dir, gust, avg, chill = sensor.get_wind_values()
    assert dir == 69
    assert gust == 0.4
    assert avg == 0.4
    assert chill == 18.9


def test_get_wind_mean_values():
    sensor = Sensor(wind_data)
    values_list = [(5, 2, 3, 5), (5, 2, 3, 5), (8, 2, 3, 8)]
    dir, gust, avg, chill = sensor.get_wind_mean_values(values_list)
    assert dir == 6
    assert gust == 2
    assert avg == 3
    assert chill == 6


def test_get_sol_value():
    sensor = Sensor(sol_data)
    rad = sensor.get_sol_value()
    assert rad == 487


def test_get_sol_mean_value():
    sensor = Sensor(sol_data)
    values_list = [5, 5, 8]
    rad = sensor.get_sol_mean_value(values_list)
    assert rad == 6


def test_get_rain_values():
    sensor = Sensor(rain_data)
    rate, total = sensor.get_rain_values()
    assert rate == 0
    assert total == 847.0


def test_get_rain_mean_values():
    sensor = Sensor(rain_data)
    value_list = [(0, 377.6), (0, 377.8), (0, 377.8)]
    rate, rain = sensor.get_rain_mean_values(value_list)
    assert rate == 0
    assert rain == 0.2


def test_get_uv_value():
    sensor = Sensor(uv_data)
    uvi = sensor.get_uv_value()
    assert uvi == 0


def test_get_uv_mean_value():
    sensor = Sensor(uv_data)
    values_list = [5, 5, 8]
    uvi = sensor.get_uv_mean_value(values_list)
    assert uvi == 6
