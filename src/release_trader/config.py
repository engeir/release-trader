"""Global constants used for logging into an account."""
import os

# import subprocess as sp
# from subprocess import check_output

# API_KEY = os.popen("pass Crypto/Binance/API_KEY")
# API_KEY = sp.Popen(["pass", "Crypto/Binance/API_KEY"], stdout=sp.PIPE, text=True)
# SECRET_KEY = os.popen("pass Crypto/Binance/SECRET_KEY")
# SECRET_KEY = sp.Popen(
#         ["pass", "Crypto/Binance/SECRET_KEY"], stdout=sp.PIPE, text=True
# )
# BINANCE_DICT = {
#     "API_KEY": API_KEY.communicate()[0].decode("utf-8")[:-1],
#     "SECRET_KEY": SECRET_KEY.communicate()[0].decode("utf-8")[:-1],
# }
# BINANCE_DICT = {
#     "API_KEY": API_KEY.read().rstrip(),
#     "SECRET_KEY": SECRET_KEY.read().rstrip(),
# }

API_KEY = os.popen("pass Crypto/Gateio/API_KEY")
SECRET_KEY = os.popen("pass Crypto/Gateio/SECRET_KEY")
GATEIO_DICT = {
    "API_KEY": API_KEY.read().rstrip(),
    "SECRET_KEY": SECRET_KEY.read().rstrip(),
}

API_KEY = os.popen("pass Crypto/Gateio_v4/API_KEY")
SECRET_KEY = os.popen("pass Crypto/Gateio_v4/SECRET_KEY")
GATEIOv4_DICT = {
    "API_KEY": API_KEY.read().rstrip(),
    "SECRET_KEY": SECRET_KEY.read().rstrip(),
}

if __name__ == "__main__":
    print(GATEIO_DICT)
