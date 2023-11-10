import requests
import psycopg2
from decouple import config
from fastapi import HTTPException
from typing import List
from app.models import Stock
from datetime import datetime
from sqlmodel import select

# test_data = {
#     "2023-11-09": {
#         "1. open": "146.5500",
#         "2. high": "146.9900",
#         "3. low": "145.2800",
#         "4. close": "146.6200",
#         "5. volume": "3412713",
#     },
#     "2023-11-08": {
#         "1. open": "149.2500",
#         "2. high": "149.6800",
#         "3. low": "147.5850",
#         "4. close": "148.0300",
#         "5. volume": "3618588",
#     },
#     "2023-11-07": {
#         "1. open": "149.0300",
#         "2. high": "149.2800",
#         "3. low": "148.0300",
#         "4. close": "148.8300",
#         "5. volume": "3549853",
#     },
#     "2023-11-06": {
#         "1. open": "147.8900",
#         "2. high": "149.2250",
#         "3. low": "147.8500",
#         "4. close": "148.9700",
#         "5. volume": "4597249",
#     },
#     "2023-11-03": {
#         "1. open": "147.4500",
#         "2. high": "148.4450",
#         "3. low": "147.2800",
#         "4. close": "147.9000",
#         "5. volume": "3510495",
#     },
#     "2023-11-02": {
#         "1. open": "145.7700",
#         "2. high": "147.1000",
#         "3. low": "144.8400",
#         "4. close": "147.0100",
#         "5. volume": "3902657",
#     },
#     "2023-11-01": {
#         "1. open": "145.0000",
#         "2. high": "146.5100",
#         "3. low": "144.4500",
#         "4. close": "145.4000",
#         "5. volume": "4750081",
#     },
#     "2023-10-31": {
#         "1. open": "143.0000",
#         "2. high": "144.7600",
#         "3. low": "142.5900",
#         "4. close": "144.6400",
#         "5. volume": "6592041",
#     },
#     "2023-10-30": {
#         "1. open": "143.1900",
#         "2. high": "144.5000",
#         "3. low": "142.5800",
#         "4. close": "142.6300",
#         "5. volume": "4204190",
#     },
#     "2023-10-27": {
#         "1. open": "143.6200",
#         "2. high": "144.7000",
#         "3. low": "141.7100",
#         "4. close": "142.5200",
#         "5. volume": "5469227",
#     },
#     "2023-10-26": {
#         "1. open": "142.2000",
#         "2. high": "144.4100",
#         "3. low": "141.5800",
#         "4. close": "143.7600",
#         "5. volume": "11130170",
#     },
#     "2023-10-25": {
#         "1. open": "137.5000",
#         "2. high": "138.4900",
#         "3. low": "136.3300",
#         "4. close": "137.0800",
#         "5. volume": "6472549",
#     },
#     "2023-10-24": {
#         "1. open": "136.7400",
#         "2. high": "137.9800",
#         "3. low": "136.0500",
#         "4. close": "137.7900",
#         "5. volume": "3697975",
#     },
#     "2023-10-23": {
#         "1. open": "136.6300",
#         "2. high": "137.6800",
#         "3. low": "135.8700",
#         "4. close": "136.3800",
#         "5. volume": "3457527",
#     },
#     "2023-10-20": {
#         "1. open": "138.1500",
#         "2. high": "139.2700",
#         "3. low": "137.1200",
#         "4. close": "137.1600",
#         "5. volume": "4865615",
#     },
#     "2023-10-19": {
#         "1. open": "138.6400",
#         "2. high": "139.4050",
#         "3. low": "137.9300",
#         "4. close": "138.0100",
#         "5. volume": "5314159",
#     },
#     "2023-10-18": {
#         "1. open": "140.0000",
#         "2. high": "140.4300",
#         "3. low": "139.5800",
#         "4. close": "139.9700",
#         "5. volume": "3329985",
#     },
#     "2023-10-17": {
#         "1. open": "137.1200",
#         "2. high": "140.6200",
#         "3. low": "136.3100",
#         "4. close": "140.3200",
#         "5. volume": "4172822",
#     },
#     "2023-10-16": {
#         "1. open": "139.2800",
#         "2. high": "139.7800",
#         "3. low": "138.5200",
#         "4. close": "139.2100",
#         "5. volume": "3361468",
#     },
#     "2023-10-13": {
#         "1. open": "139.7700",
#         "2. high": "140.1200",
#         "3. low": "138.2700",
#         "4. close": "138.4600",
#         "5. volume": "4583553",
#     },
#     "2023-10-12": {
#         "1. open": "142.5100",
#         "2. high": "142.9300",
#         "3. low": "140.9500",
#         "4. close": "141.2400",
#         "5. volume": "3921142",
#     },
#     "2023-10-11": {
#         "1. open": "142.5100",
#         "2. high": "143.3400",
#         "3. low": "142.1400",
#         "4. close": "143.2300",
#         "5. volume": "2511459",
#     },
#     "2023-10-10": {
#         "1. open": "142.6000",
#         "2. high": "143.4150",
#         "3. low": "141.7200",
#         "4. close": "142.1100",
#         "5. volume": "3015784",
#     },
#     "2023-10-09": {
#         "1. open": "142.3000",
#         "2. high": "142.4000",
#         "3. low": "140.6800",
#         "4. close": "142.2000",
#         "5. volume": "2354396",
#     },
#     "2023-10-06": {
#         "1. open": "141.4000",
#         "2. high": "142.9400",
#         "3. low": "140.1100",
#         "4. close": "142.0300",
#         "5. volume": "3511347",
#     },
#     "2023-10-05": {
#         "1. open": "140.9000",
#         "2. high": "141.7000",
#         "3. low": "140.1900",
#         "4. close": "141.5200",
#         "5. volume": "3223910",
#     },
#     "2023-10-04": {
#         "1. open": "140.3700",
#         "2. high": "141.2004",
#         "3. low": "139.9900",
#         "4. close": "141.0700",
#         "5. volume": "2637779",
#     },
#     "2023-10-03": {
#         "1. open": "140.8700",
#         "2. high": "141.6400",
#         "3. low": "140.0000",
#         "4. close": "140.3900",
#         "5. volume": "3284421",
#     },
#     "2023-10-02": {
#         "1. open": "140.0400",
#         "2. high": "141.4500",
#         "3. low": "139.8600",
#         "4. close": "140.8000",
#         "5. volume": "3275461",
#     },
#     "2023-09-29": {
#         "1. open": "142.0000",
#         "2. high": "142.1300",
#         "3. low": "139.6100",
#         "4. close": "140.3000",
#         "5. volume": "5703983",
#     },
#     "2023-09-28": {
#         "1. open": "142.1400",
#         "2. high": "142.2820",
#         "3. low": "140.2050",
#         "4. close": "141.5800",
#         "5. volume": "5783422",
#     },
#     "2023-09-27": {
#         "1. open": "143.6700",
#         "2. high": "143.8200",
#         "3. low": "141.7600",
#         "4. close": "143.1700",
#         "5. volume": "4439121",
#     },
#     "2023-09-26": {
#         "1. open": "145.5100",
#         "2. high": "146.1700",
#         "3. low": "143.0201",
#         "4. close": "143.2400",
#         "5. volume": "4824654",
#     },
#     "2023-09-25": {
#         "1. open": "146.5700",
#         "2. high": "147.4300",
#         "3. low": "146.2500",
#         "4. close": "146.4800",
#         "5. volume": "2694245",
#     },
#     "2023-09-22": {
#         "1. open": "147.4100",
#         "2. high": "148.1000",
#         "3. low": "146.8200",
#         "4. close": "146.9100",
#         "5. volume": "2562216",
#     },
#     "2023-09-21": {
#         "1. open": "149.0000",
#         "2. high": "149.2500",
#         "3. low": "147.3100",
#         "4. close": "147.3800",
#         "5. volume": "4944786",
#     },
#     "2023-09-20": {
#         "1. open": "148.3600",
#         "2. high": "151.9299",
#         "3. low": "148.1300",
#         "4. close": "149.8300",
#         "5. volume": "9636681",
#     },
#     "2023-09-19": {
#         "1. open": "145.0000",
#         "2. high": "146.7200",
#         "3. low": "144.6600",
#         "4. close": "146.5200",
#         "5. volume": "3945423",
#     },
#     "2023-09-18": {
#         "1. open": "145.7700",
#         "2. high": "146.4800",
#         "3. low": "145.0600",
#         "4. close": "145.0900",
#         "5. volume": "2508062",
#     },
#     "2023-09-15": {
#         "1. open": "147.1100",
#         "2. high": "147.8500",
#         "3. low": "145.5300",
#         "4. close": "145.9900",
#         "5. volume": "6234033",
#     },
#     "2023-09-14": {
#         "1. open": "147.3800",
#         "2. high": "147.7300",
#         "3. low": "146.4800",
#         "4. close": "147.3500",
#         "5. volume": "2723200",
#     },
#     "2023-09-13": {
#         "1. open": "145.9500",
#         "2. high": "146.9800",
#         "3. low": "145.9200",
#         "4. close": "146.5500",
#         "5. volume": "2627999",
#     },
#     "2023-09-12": {
#         "1. open": "147.9200",
#         "2. high": "148.0000",
#         "3. low": "145.8000",
#         "4. close": "146.3000",
#         "5. volume": "4457695",
#     },
#     "2023-09-11": {
#         "1. open": "148.5700",
#         "2. high": "148.7800",
#         "3. low": "147.5800",
#         "4. close": "148.3800",
#         "5. volume": "3273720",
#     },
#     "2023-09-08": {
#         "1. open": "147.3500",
#         "2. high": "148.5900",
#         "3. low": "147.2600",
#         "4. close": "147.6800",
#         "5. volume": "3722927",
#     },
#     "2023-09-07": {
#         "1. open": "148.1300",
#         "2. high": "148.7800",
#         "3. low": "147.4000",
#         "4. close": "147.5200",
#         "5. volume": "3333040",
#     },
#     "2023-09-06": {
#         "1. open": "147.6600",
#         "2. high": "148.3300",
#         "3. low": "147.1200",
#         "4. close": "148.0600",
#         "5. volume": "2932203",
#     },
#     "2023-09-05": {
#         "1. open": "147.9100",
#         "2. high": "149.0000",
#         "3. low": "147.5719",
#         "4. close": "148.1300",
#         "5. volume": "3731281",
#     },
#     "2023-09-01": {
#         "1. open": "147.2600",
#         "2. high": "148.1000",
#         "3. low": "146.9200",
#         "4. close": "147.9400",
#         "5. volume": "2727796",
#     },
#     "2023-08-31": {
#         "1. open": "146.9400",
#         "2. high": "147.7275",
#         "3. low": "146.5400",
#         "4. close": "146.8300",
#         "5. volume": "3885949",
#     },
#     "2023-08-30": {
#         "1. open": "146.4200",
#         "2. high": "146.9200",
#         "3. low": "145.7452",
#         "4. close": "146.8600",
#         "5. volume": "2245402",
#     },
#     "2023-08-29": {
#         "1. open": "146.3000",
#         "2. high": "146.7300",
#         "3. low": "145.6200",
#         "4. close": "146.4500",
#         "5. volume": "2778113",
#     },
#     "2023-08-28": {
#         "1. open": "145.4100",
#         "2. high": "146.7400",
#         "3. low": "145.2100",
#         "4. close": "146.0200",
#         "5. volume": "3561347",
#     },
#     "2023-08-25": {
#         "1. open": "144.1800",
#         "2. high": "145.4700",
#         "3. low": "143.5000",
#         "4. close": "145.3500",
#         "5. volume": "3660147",
#     },
#     "2023-08-24": {
#         "1. open": "143.5050",
#         "2. high": "144.4700",
#         "3. low": "143.2200",
#         "4. close": "143.5500",
#         "5. volume": "2900244",
#     },
#     "2023-08-23": {
#         "1. open": "141.7200",
#         "2. high": "143.4750",
#         "3. low": "141.5800",
#         "4. close": "143.4100",
#         "5. volume": "2559083",
#     },
#     "2023-08-22": {
#         "1. open": "142.6600",
#         "2. high": "143.2250",
#         "3. low": "141.3000",
#         "4. close": "141.4900",
#         "5. volume": "3557734",
#     },
#     "2023-08-21": {
#         "1. open": "141.4200",
#         "2. high": "142.3900",
#         "3. low": "141.1100",
#         "4. close": "142.2800",
#         "5. volume": "2937781",
#     },
#     "2023-08-18": {
#         "1. open": "140.0000",
#         "2. high": "141.8300",
#         "3. low": "139.7600",
#         "4. close": "141.4100",
#         "5. volume": "3915480",
#     },
#     "2023-08-17": {
#         "1. open": "141.0100",
#         "2. high": "142.6600",
#         "3. low": "140.6000",
#         "4. close": "140.6600",
#         "5. volume": "3742058",
#     },
#     "2023-08-16": {
#         "1. open": "141.7000",
#         "2. high": "142.0900",
#         "3. low": "140.5600",
#         "4. close": "140.6400",
#         "5. volume": "3285347",
#     },
#     "2023-08-15": {
#         "1. open": "141.5000",
#         "2. high": "142.3100",
#         "3. low": "141.2000",
#         "4. close": "141.8700",
#         "5. volume": "3656559",
#     },
#     "2023-08-14": {
#         "1. open": "143.0500",
#         "2. high": "143.3650",
#         "3. low": "141.8020",
#         "4. close": "141.9100",
#         "5. volume": "4226563",
#     },
#     "2023-08-11": {
#         "1. open": "143.1200",
#         "2. high": "143.4500",
#         "3. low": "142.2050",
#         "4. close": "143.1200",
#         "5. volume": "2526433",
#     },
#     "2023-08-10": {
#         "1. open": "143.0400",
#         "2. high": "144.5800",
#         "3. low": "142.6900",
#         "4. close": "143.2500",
#         "5. volume": "4735763",
#     },
#     "2023-08-09": {
#         "1. open": "144.9400",
#         "2. high": "144.9400",
#         "3. low": "142.3000",
#         "4. close": "142.4900",
#         "5. volume": "4073038",
#     },
#     "2023-08-08": {
#         "1. open": "145.7000",
#         "2. high": "146.1500",
#         "3. low": "144.1100",
#         "4. close": "145.9100",
#         "5. volume": "4654582",
#     },
#     "2023-08-07": {
#         "1. open": "145.0000",
#         "2. high": "146.5000",
#         "3. low": "144.9300",
#         "4. close": "146.1800",
#         "5. volume": "3438654",
#     },
#     "2023-08-04": {
#         "1. open": "145.0900",
#         "2. high": "146.0900",
#         "3. low": "143.9900",
#         "4. close": "144.2400",
#         "5. volume": "4223204",
#     },
#     "2023-08-03": {
#         "1. open": "143.7800",
#         "2. high": "145.2200",
#         "3. low": "143.3116",
#         "4. close": "144.4500",
#         "5. volume": "3952640",
#     },
#     "2023-08-02": {
#         "1. open": "142.7800",
#         "2. high": "144.3000",
#         "3. low": "142.3100",
#         "4. close": "144.1700",
#         "5. volume": "4959381",
#     },
#     "2023-08-01": {
#         "1. open": "144.2500",
#         "2. high": "144.4800",
#         "3. low": "142.1700",
#         "4. close": "143.3300",
#         "5. volume": "4798703",
#     },
#     "2023-07-31": {
#         "1. open": "143.8100",
#         "2. high": "144.6050",
#         "3. low": "143.5300",
#         "4. close": "144.1800",
#         "5. volume": "6138902",
#     },
#     "2023-07-28": {
#         "1. open": "143.4400",
#         "2. high": "143.9500",
#         "3. low": "142.8500",
#         "4. close": "143.4500",
#         "5. volume": "6686627",
#     },
#     "2023-07-27": {
#         "1. open": "142.3000",
#         "2. high": "143.3800",
#         "3. low": "141.9000",
#         "4. close": "142.9700",
#         "5. volume": "6331563",
#     },
#     "2023-07-26": {
#         "1. open": "140.4400",
#         "2. high": "141.2500",
#         "3. low": "139.8800",
#         "4. close": "141.0700",
#         "5. volume": "4046441",
#     },
#     "2023-07-25": {
#         "1. open": "139.4200",
#         "2. high": "140.4300",
#         "3. low": "139.0403",
#         "4. close": "140.3300",
#         "5. volume": "3770813",
#     },
#     "2023-07-24": {
#         "1. open": "139.3500",
#         "2. high": "140.1200",
#         "3. low": "138.7788",
#         "4. close": "139.5400",
#         "5. volume": "3475442",
#     },
#     "2023-07-21": {
#         "1. open": "138.2100",
#         "2. high": "139.7799",
#         "3. low": "137.7600",
#         "4. close": "138.9400",
#         "5. volume": "5858741",
#     },
#     "2023-07-20": {
#         "1. open": "137.1900",
#         "2. high": "140.3200",
#         "3. low": "136.5600",
#         "4. close": "138.3800",
#         "5. volume": "10896330",
#     },
#     "2023-07-19": {
#         "1. open": "135.5300",
#         "2. high": "136.4500",
#         "3. low": "135.1900",
#         "4. close": "135.4800",
#         "5. volume": "5519992",
#     },
#     "2023-07-18": {
#         "1. open": "134.7100",
#         "2. high": "135.9500",
#         "3. low": "134.2900",
#         "4. close": "135.3600",
#         "5. volume": "3852058",
#     },
#     "2023-07-17": {
#         "1. open": "133.2600",
#         "2. high": "134.6100",
#         "3. low": "133.1000",
#         "4. close": "134.2400",
#         "5. volume": "3168419",
#     },
#     "2023-07-14": {
#         "1. open": "133.9100",
#         "2. high": "133.9200",
#         "3. low": "132.9400",
#         "4. close": "133.4000",
#         "5. volume": "2861496",
#     },
#     "2023-07-13": {
#         "1. open": "133.5100",
#         "2. high": "135.0700",
#         "3. low": "133.3600",
#         "4. close": "133.9200",
#         "5. volume": "3221422",
#     },
#     "2023-07-12": {
#         "1. open": "135.0700",
#         "2. high": "135.3300",
#         "3. low": "132.5750",
#         "4. close": "132.8400",
#         "5. volume": "3732189",
#     },
#     "2023-07-11": {
#         "1. open": "133.6600",
#         "2. high": "134.5600",
#         "3. low": "133.2300",
#         "4. close": "134.4400",
#         "5. volume": "2925238",
#     },
#     "2023-07-10": {
#         "1. open": "131.7600",
#         "2. high": "133.0500",
#         "3. low": "131.6950",
#         "4. close": "132.9000",
#         "5. volume": "2369425",
#     },
#     "2023-07-07": {
#         "1. open": "131.7800",
#         "2. high": "133.8550",
#         "3. low": "131.7500",
#         "4. close": "132.0800",
#         "5. volume": "2982738",
#     },
#     "2023-07-06": {
#         "1. open": "133.2350",
#         "2. high": "133.9000",
#         "3. low": "131.5500",
#         "4. close": "132.1600",
#         "5. volume": "3508083",
#     },
#     "2023-07-05": {
#         "1. open": "133.3200",
#         "2. high": "134.3100",
#         "3. low": "132.5900",
#         "4. close": "134.2400",
#         "5. volume": "2955870",
#     },
#     "2023-07-03": {
#         "1. open": "133.4200",
#         "2. high": "134.3500",
#         "3. low": "132.8700",
#         "4. close": "133.6700",
#         "5. volume": "1477149",
#     },
#     "2023-06-30": {
#         "1. open": "134.6900",
#         "2. high": "135.0300",
#         "3. low": "133.4250",
#         "4. close": "133.8100",
#         "5. volume": "4236677",
#     },
#     "2023-06-29": {
#         "1. open": "131.7500",
#         "2. high": "134.3500",
#         "3. low": "131.6900",
#         "4. close": "134.0600",
#         "5. volume": "3639836",
#     },
#     "2023-06-28": {
#         "1. open": "132.0600",
#         "2. high": "132.1700",
#         "3. low": "130.9100",
#         "4. close": "131.7600",
#         "5. volume": "2753779",
#     },
#     "2023-06-27": {
#         "1. open": "131.3000",
#         "2. high": "132.9500",
#         "3. low": "130.8300",
#         "4. close": "132.3400",
#         "5. volume": "3219909",
#     },
#     "2023-06-26": {
#         "1. open": "129.3900",
#         "2. high": "131.4100",
#         "3. low": "129.3100",
#         "4. close": "131.3400",
#         "5. volume": "4845649",
#     },
#     "2023-06-23": {
#         "1. open": "130.4000",
#         "2. high": "130.6200",
#         "3. low": "129.1800",
#         "4. close": "129.4300",
#         "5. volume": "11324705",
#     },
#     "2023-06-22": {
#         "1. open": "131.6800",
#         "2. high": "132.9600",
#         "3. low": "130.6800",
#         "4. close": "131.1700",
#         "5. volume": "6013021",
#     },
#     "2023-06-21": {
#         "1. open": "135.1100",
#         "2. high": "135.3900",
#         "3. low": "133.2900",
#         "4. close": "133.6900",
#         "5. volume": "5501272",
#     },
# }


async def get_symbol_data(symbol: str):
    api_key = config("ALPHA_VANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if "Error Message" in data:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found!")

    return [
        {
            "date": x[0],
            "open": x[1].get("1. open"),
            "high": x[1].get("2. high"),
            "low": x[1].get("3. low"),
            "close": x[1].get("4. close"),
            "volume": x[1].get("5. volume"),
            "ticker": symbol,
        }
        for x in data["Time Series (Daily)"].items()
    ]


async def insert_symbol_data(symbol_data: List[Stock], database):
    data = [Stock(**x) for x in symbol_data]
    [database.add(x) for x in data]
    database.commit()
    return symbol_data


# Get new data missing
def get_new_data(get_symbol_data, database_data: List[Stock]):
    last_date = max([x.date for x in database_data])
    return [
        x
        for x in get_symbol_data
        if datetime.strptime(x["date"], "%Y-%m-%d").date() > last_date
    ]


async def get_unique_symbols(database):
    query = database.exec(select(Stock.ticker).distinct())
    return [row for row in query]
