import hmac, datetime
from .data import constants as c


def sign(message, secret_key):
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    return mac.hexdigest()


# timestamp + "#" + memo + "#" + queryString
def pre_substring(timestamp, memo, body):
    return f'{str(timestamp)}#{memo}#{body}'


def get_header(api_key, sign, timestamp):
    header = dict()
    header[c.CONTENT_TYPE] = c.APPLICATION_JSON
    header[c.USER_AGENT] = c.VERSION

    if api_key:
        header[c.X_BM_KEY] = api_key
    if sign:
        header[c.X_BM_SIGN] = sign
    if timestamp:
        header[c.X_BM_TIMESTAMP] = str(timestamp)

    return header


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'

    return url[0:-1]


def get_timestamp():
    return str(int(datetime.datetime.now().timestamp() * 1000))


def round_time(dt=None, round_to=60):
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


def get_kline_time(kline_type: c.BtFuturesSocketKlineChannels):
    items = kline_type.name.split("_")
    tf_name = items[-1].lower().replace("min", "m").replace("day", "d").replace("week", "w"). \
        replace("hours", "h").replace("hour", "h")
    # tf = c.TimeFrame.__dict__[f'tf_{tf_name}']
    now_ = datetime.datetime.now()
    now_ = now_.replace(second=0, microsecond=0)
    tf_val = int(tf_name[:-1])
    if "m" in tf_name:
        cm, _ = divmod(now_.minute, tf_val)
        return now_.replace(minute=cm * tf_val)
    now_ = now_.replace(minute=0)
    if "h" in tf_name:
        ch, _ = divmod(now_.hour, tf_val)
        return now_.replace(hour=ch * tf_val)
    now_ = now_.replace(hour=0)
    # TODO: weeks not implemented
    return now_
