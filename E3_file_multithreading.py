import concurrent.futures
import datetime
import os
from concurrent.futures import ThreadPoolExecutor, wait

import pytz
import requests
import time

def create_file_name_country(base_prefix: str):
    if not os.path.exists(base_prefix):
        os.makedirs(base_prefix)

    executor = ThreadPoolExecutor(max_workers=20)
    futures = []

    for name in names_l:
        file_path = os.path.join(base_prefix, f"{name}.txt")

        future = executor.submit(main, name, file_path)
        futures.append(future)

    done, not_done = wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
    print(f"done: {len(done)}, not done: {len(not_done)}")


def get_dict_for_name(name, url_path):
    response = requests.get(url_path, params={'name': name})

    if response.status_code < 400:
        name_country_dict = response.json()
        return name_country_dict
    else:
        raise Exception(f"error: {response.status_code}")

def get_max_prob_country(name_country_dict):
    sorted_country_probability = sorted(name_country_dict['country'], key=lambda d: d['probability'], reverse=True)
    country_max_probability = sorted_country_probability[0]['country_id']
    return country_max_probability

def get_country_url(url_path, country_max_probability):
    COUNTRY_URL = f'{url_path}/{country_max_probability}'
    response_c = requests.get(COUNTRY_URL)
    if response_c.status_code == 200:
        country_id2name = response_c.json()
        return country_id2name
    else:
        raise Exception(f"error: {response_c.status_code}")

def get_country_name(country_id2name):
    country_name = country_id2name[0]['name']['common']
    # print(country_name)
    # print(f"most probable country of your name: {country_name}")
    return country_name


def main(name, file_path):
    name_country_dict = get_dict_for_name(name, COUNTRILIZE_URL)
    country_max_probability = get_max_prob_country(name_country_dict)
    country_id2name = get_country_url(COUNTRY_URL, country_max_probability)
    country_name = get_country_name(country_id2name)
    name_and_country = (name, country_name)
    write_to_file(file_path, name, name_and_country)

def write_to_file(file_path, name, name_and_country):
    with open(file_path, 'w') as file_h:
        file_h.writelines(f"name and nationality: {name_and_country}")


if __name__ == '__main__':
    try:
        with open('C:\\Users\\tamar\Desktop\\full stack course\Requests\\names.txt', 'r') as fh:
            content = fh.read()
            names_l = content.split(", ")

        COUNTRILIZE_URL = 'https://api.nationalize.io'
        COUNTRY_URL = f'https://restcountries.com/v3.1/alpha'

        start = time.time()

        create_file_name_country('C:\\Users\\tamar\Desktop\\full stack course\Requests\\name_country')
        end = time.time()
        print("")
        print(f"total time: {end - start} sec")


    except Exception as e:
        print(e)
    finally:
        fh.close()