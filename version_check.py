# /MyUtils/myutils/version_check.py

import requests


def get_latest_version():
    url = 'https://api.github.com/repos/eliawaefler/MyUtils/releases/latest'
    response = requests.get(url)
    latest_version = response.json().get('tag_name')
    return latest_version


def check_version():
    import myutils
    current_version = myutils.__version__
    latest_version = get_latest_version()

    if current_version != latest_version:
        print(
            f"WARNING: You are using MyUtils version {current_version}, "
            f"but version {latest_version} is available. Please update to the latest version.")
