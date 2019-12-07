import tempfile

import pandas as pd
import requests

BEGIN_MARKER = 'Сумма(р)'
END_MARKER = 'Unnamed'
ITEMS_COLUMN = 'Наименование'
BUY_EVENT_MARKER = 1


def load_gsheet(sheet_url):
    with tempfile.NamedTemporaryFile(suffix='.csv') as tfile:
        with open(tfile.name, 'wb') as f:
            f.write(requests.get(sheet_url).content)
        return pd.read_csv(tfile.name, skiprows=1)


def extract_users(df):
    begin_column = df.columns.tolist().index(BEGIN_MARKER)
    end_column = min([
        i
        for i, name in enumerate(df.columns.tolist())
        if name.startswith(END_MARKER)
    ])
    return df[df.columns[begin_column + 1:end_column]]


def extract_items(df):
    return df[ITEMS_COLUMN]


def get_order(sheet_url, user_name):
    df = load_gsheet(sheet_url)
    users = extract_users(df)
    items = extract_items(df)

    user_items = items[users[user_name] == BUY_EVENT_MARKER].tolist()
    return user_items


def main(sheet_url):
    df = load_gsheet(sheet_url)
    users = extract_users(df)
    items = extract_items(df)

    for user in users.columns:
        user_items = items[users[user] == BUY_EVENT_MARKER].tolist()
        if len(user_items) > 0:
            print(f'>> {user}')
            print(user_items)
            print('')


if __name__ == '__main__':
    main(
        sheet_url='https://docs.google.com/spreadsheets/d/1p-Xs3UB8HaVkauVS-K6Wko2T_0txNILp/export?format=csv&id=1p-Xs3UB8HaVkauVS-K6Wko2T_0txNILp&gid=1128347462')
