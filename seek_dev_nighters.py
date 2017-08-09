import requests
import datetime
import pytz
import collections
import tqdm


def load_attempts():
    url = 'https://devman.org/api/challenges/solution_attempts/'
    page = 1
    while True:
        response = requests.get(url=url.format(page), params={'page': page}).json()
        yield response['records']
        number_of_pages = response['number_of_pages']
        page += 1
        if page > int(number_of_pages):
            break


def convert_data(data_list):
    converted_list = []
    for element in data_list:
        if not element['timestamp']:
            continue
        time = datetime.datetime.fromtimestamp(element['timestamp'], pytz.timezone(element['timezone']))
        converted_list.append((element['username'], time))
    return converted_list


def get_owls(data_list):
    return collections.Counter([user for user, time in data_list if 0 <= time.hour < 5])


def print_owls(users_counter):
    print('Following users send their solutions after midnight:')
    print('\n'.join(['"{}" {} times'.format(name, count)
                     for name, count in sorted(users_counter.items(), key=lambda x: x[1], reverse=True)]))

if __name__ == '__main__':
    api_data = []
    [api_data.extend(x) for x in tqdm.tqdm(load_attempts(), desc='collecting data')]
    data_with_time = convert_data(api_data)
    owls = get_owls(data_with_time)
    print_owls(owls)
