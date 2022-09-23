import pandas as pd


def get_pm25(sort=False):
    url = 'https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV'
    df = pd.read_csv(url).dropna()[
        ' county site		pm25	datacreationdate'.split()]
    # print(df)
    if sort:
        df = df.sort_values('pm25', ascending=False)

    return df.columns.tolist(), df.values.tolist()


# print(get_pm25())
