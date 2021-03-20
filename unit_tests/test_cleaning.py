import pandas as pd
from modules.cleaning import clean_up_data_set

DF_SCHEMA = {'timestamp': 'datetime64[ns, UTC]',
             'country_code': 'string',
             'last_order_ts': 'datetime64[ns, UTC]',
             'total_orders': 'int',
             'voucher_amount': 'int', }


def test_clean_up_data_set():
    df = pd.DataFrame(
        {'timestamp':
             ['2020-12-11 18:36:46.623720+00:00',
              '2020-12-11 18:36:46.623720+00:00',
              '2020-12-11 18:36:46.623720+00:00'],
         'country_code': ['Peru', 'Peru', 'Peru'],
         'last_order_ts': ['2020-11-11 00:00:00+00:00', '2020-11-11 00:00:00+00:00', 'AAA'],
         'first_order_ts': [1560211200000000, 1560211200000000, 'BBB'],
         'total_orders': [10.0, 10.0, 'TTT'],
         'voucher_amount': [5.0, 5.0, 5.0],
         'additional column': ['aaaa', 'bbbb', 'bbbb'],
         }
    )
    df_expected = pd.DataFrame(
        {'timestamp': ['2020-12-11 18:36:46.623720+00:00'],
         'country_code': ['Peru'],
         'last_order_ts': ['2020-11-11 00:00:00'],
         'total_orders': [10],
         'voucher_amount': [5],
         }
    ).astype(DF_SCHEMA)

    result_df = clean_up_data_set(df, DF_SCHEMA)

    assert result_df.equals(df_expected)
