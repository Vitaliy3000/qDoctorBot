import datetime


def calc_delta():
    pass


def add_delta():
    pass


def parse_datetime_emias(string: str) -> datetime.datetime:
    return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S+03:00')


def datetime_to_emias_format(datetime_: datetime.datetime) -> str:
    return datetime_.strftime('%Y-%m-%dT%H:%M:%S+03:00')


def compress_datetime(datetime_: datetime.datetime) -> str:
    return datetime_.strftime('%Y%m%d%H%M%S')


def uncompress_datetime(string: str) -> datetime.datetime:
    return datetime.datetime.strptime(string, '%Y%m%d%H%M%S')