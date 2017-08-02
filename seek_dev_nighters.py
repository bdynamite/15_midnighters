import requests
import datetime
import pytz
import collections
import tqdm


def load_attempts():
    pages = 10
    url = 'https://devman.org/api/challenges/solution_attempts/'
    records_list = []
    for page in tqdm.tqdm(range(pages), desc='collecting data'):
        responce = requests.get(url=url.format(page), params={'page': page + 1})
        records_list.extend(responce.json()['records'])
    return records_list


def convert_data(data_list):
    converted_list = []
    for element in data_list:
        if not element['timestamp']:
            continue
        time = datetime.datetime.fromtimestamp(element['timestamp'], pytz.timezone(element['timezone']))
        converted_list.append((element['username'], time))
    return converted_list


def get_midnighters(data_list):
    midnighters = collections.Counter([x[0] for x in data_list if x[1].hour in range(5)])
    return midnighters


def print_midnighters(midnighters):
    print('Following users send their solutions after midnight:')
    print('\n'.join(['"{}" {} times'.format(x[0], x[1])
                     for x in sorted(midnighters.items(), key=lambda y: y[1], reverse=True)]))

if __name__ == '__main__':
    api_data = load_attempts()
    data_with_time = convert_data(api_data)
    midnighters = get_midnighters(data_with_time)
    print_midnighters(midnighters)

