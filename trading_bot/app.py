import json
import requests
import hmac
import hashlib
import time

BASE_URL = "https://api.crypto.com/v2/"
API_KEY = ""
SECRET_KEY = ""

with open("trading_bot/keys.json") as keys:
  info = json.load(keys)
  API_KEY = info["api_key"]
  SECRET_KEY = info["secret_key"]

def get_candlestick(instrument_name, timeframe):
  info = requests.get(BASE_URL+"public/get-candlestick?instrument_name=" + instrument_name + "&timeframe=" + timeframe)
  info = json.loads(info.text)
  return info["result"]["data"][-1]

latest_candlestick_eth_usdt = get_candlestick("ETH_USDT","5m")
print(latest_candlestick_eth_usdt)

# t : timestand
# o : opening value
# h : hightest value
# l : lowest value
# c : closing value
# v : volume

def get_order_history():
  req = {
      "id": 11,
      "method": "private/get-order-history",
      "api_key": API_KEY,
      "params": {},
      "nonce": int(time.time() * 1000)
  }

  # First ensure the params are alphabetically sorted by key
  param_str = ""

  MAX_LEVEL = 3


  def params_to_str(obj, level):
      if level >= MAX_LEVEL:
          return str(obj)

      return_str = ""
      for key in sorted(obj):
          return_str += key
          if isinstance(obj[key], list):
              for subObj in obj[key]:
                  return_str += params_to_str(subObj, ++level)
          else:
              return_str += str(obj[key])
      return return_str


  if "params" in req:
      param_str = params_to_str(req['params'], 0)

  payload_str = req['method'] + str(req['id']) + req['api_key'] + param_str + str(req['nonce'])

  req['sig'] = hmac.new(
      bytes(str(SECRET_KEY), 'utf-8'),
      msg=bytes(payload_str, 'utf-8'),
      digestmod=hashlib.sha256
  ).hexdigest()

  order_history = requests.post(BASE_URL + 'private/get-order-history', json=req, headers={'Content-Type':'application/json'})
  return order_history

my_order_history = json.loads(get_order_history().text)
print(my_order_history)