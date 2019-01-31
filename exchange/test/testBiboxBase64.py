import base64
import gzip

msg = [{
    "channel":
    "bibox_sub_spot_ETC_USDT_kline_1min",
    "binary":
    "1",
    "data_type":
    1,
    "data":
    "H4sIAAAAAAAA/4quVirJzE1VsjI0NbGwNDQ1MjEwMDDQUcovSM1TslIy1rM0NzRW0lHKyEzPQObn5Jcjc5Nz8otTkQXK8nOUrJQM9CyNjQwNjC0slWp10GwyNqCuTQZQoFQbCwgAAP//DLxDSdUAAAA="
}]

str = msg[0]["data"]
data = base64.b64decode(str)
s = gzip.decompress(data).decode('utf-8')
print(s)
