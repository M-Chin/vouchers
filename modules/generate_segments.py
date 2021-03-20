import pandas as pd
from modules.segment_definitions \
    import get_recency_segment, get_frequent_segment, add_additional_columns
from modules.cleaning import find_dirt, clean_up_data_set

pd.options.mode.chained_assignment = None  # default='warn'

# Expected schema (first_order_ts not needed to calculated the segments)
DF_SCHEMA = {'timestamp': 'datetime64[ns, UTC]',
             'country_code': 'string',
             'last_order_ts': 'datetime64[ns, UTC]',
             'total_orders': 'int',
             'voucher_amount': 'int', }

# Segment names and column to check
SEGMENTS = {'frequent_segment': 'total_orders',
            'recency_segment': 'days_since_order'}

ACTIVE_COUNTRIES = ['Peru']


# Load parquet data
def load_data_set():
    df = pd.read_parquet('data.parquet.gzip', engine='pyarrow')
    return df


# Get df for specified country
def get_country_df(df, country_code):
    return df.loc[df['country_code'] == country_code]


# Get most used voucher amount per segment variation, return lowest amount in case of a tie
def get_most_used_voucher_per_segment(df, col):
    df_usage = df.groupby([col, 'voucher_amount'], as_index=False).size()
    return df_usage.loc[df_usage.groupby([col])['size'].idxmax()].sort_values(by=[col]).reset_index(drop=True)


# Build segments based on data frame
def build_segments(df, segments_col):
    seg_result = {}

    # Attribute segment variation using the definitions in 'modules.segment_definitions'
    for segment in segments_col.keys():
        if segment == 'frequent_segment':
            df[segment] = df[segments_col[segment]].map(get_frequent_segment)
        elif segment == 'recency_segment':
            df[segment] = df[segments_col[segment]].map(get_recency_segment)

    # Generate a df per segment and remove rows with not segment variant assigned
    for segment in segments_col.keys():
        df_filtered = df[(df[segment] != 'no_segment')]
        seg_result[segment] = get_most_used_voucher_per_segment(df_filtered, segment)

    return seg_result


class SegmentVouchers(object):
    def __init__(self):
        self.voucher_values = {}

    def generate_segments(self):
        df_schema = DF_SCHEMA
        segments = SEGMENTS
        countries = ACTIVE_COUNTRIES

        # Start pipeline
        # 1. Load data
        df = load_data_set()

        # 2. Clean data
        find_dirt(df, df_schema)
        df = clean_up_data_set(df, df_schema)

        # 3. Prepare data
        for country in countries:
            df2 = get_country_df(df, country)
            df2 = add_additional_columns(df2)
            # 4. Calculate segments from data
            self.voucher_values.update({country: build_segments(df2, segments)})

        for country in countries:
            for i in segments.keys():
                print(self.voucher_values[country][i])

        # End pipeline

    def get_voucher_values(self):
        return self.voucher_values
