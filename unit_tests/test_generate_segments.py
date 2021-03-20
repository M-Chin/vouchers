from modules.generate_segments import build_segments, get_most_used_voucher_per_segment
from modules.segment_definitions import get_frequent_segment, get_recency_segment
import pandas as pd


def test_get_frequent_segment():
    input_values = [0, 1, 5, 13, 20, 99, -10]

    results = []

    for value in input_values:
        results.append(get_frequent_segment(value))

    expected_values = ['0-4', '0-4', '5-13', '5-13', '13-37', 'no_segment', 'no_segment']

    assert results == expected_values


def test_get_recency_segment():
    input_values = [0, 32, 60, 70, 90, 120, 151, -10, 9999]

    results = []

    for value in input_values:
        results.append(get_recency_segment(value))

    expected_values = ['no_segment', '30-60', '30-60', '60-90', '60-90', '90-120', '120-180', 'no_segment', '180+']

    assert results == expected_values


def test_get_most_used_voucher_per_segment():
    col = 'frequent_segment'

    df = pd.DataFrame({
        'frequent_segment': ['0-4', '0-4', '0-4', '13-37', '13-37'],
        'recency_segment': ['30-60', '30-60', '60-90', '60-90', '60-90'],
        'voucher_amount': [10, 10, 99999, 111, 888]
    })

    expected_df = pd.DataFrame({
        'frequent_segment': ['0-4', '13-37'],
        'voucher_amount': [10, 111],
        'size': [2, 1]
    })

    result_df = get_most_used_voucher_per_segment(df, col)

    assert result_df.equals(expected_df)


def test_build_segments():
    segments = {'frequent_segment': 'total_orders',
                'recency_segment': 'days_since_order'}

    df = pd.DataFrame({
        'total_orders': [2, 2, 2, 20, 21, 23, 21, 23, 35, 2, 2, 2, 2],
        'days_since_order': [35, 35, 35, 35, 35, 35, 35, 35, 35, 100, 101, 130, 200],
        'voucher_amount': [10, 999999, 10, 123, 123, 123, 123, 900, 900, 888, 777, 1111, 2222]
    })

    expected_result = {'frequent_segment': pd.DataFrame({'frequent_segment': ['0-4', '13-37'],
                                                         'voucher_amount': [10, 123],
                                                         'size': [2, 4]}).sort_values(
                                                        by=['frequent_segment']).reset_index(drop=True),
                       'recency_segment': pd.DataFrame({'recency_segment': ['30-60', '90-120', '120-180', '180+'],
                                                        'voucher_amount': [123, 777, 1111, 2222],
                                                        'size': [4, 1, 1, 1]}).sort_values(
                                                        by=['recency_segment']).reset_index(drop=True)}

    result = build_segments(df, segments)

    assert all(result[i].equals(expected_result[i]) for i in segments.keys())

