import pandas as pd


# Check for dirty data
def find_dirt(df, df_schema):
    print('Checking dataset...')
    # Check duplicated rows on expected columns
    if len(df[list(df_schema.keys())].value_counts() >= 1):
        print('Found duplicated rows, clean up!')

    # Check if contains values that can not be casted properly
    for key in df_schema.keys():
        if df_schema[key] == 'int':
            if len(df[pd.to_numeric(df[key], errors='coerce').isna()]) > 0:
                print('Key {} contains invalid values!'.format(key))
        elif df_schema[key] == 'datetime64[ns, UTC]':
            if len(df[pd.to_datetime(df[key], format='%Y-%m-%d', errors='coerce').isna()]) > 0:
                print('Key {} contains invalid values!'.format(key))
            else:
                print('Key {} passed cast test.'.format(key))


# Clean the data frame and cast to correct data types
def clean_up_data_set(df, df_schema):
    # Get relevant keys only
    df = df[list(df_schema.keys())]

    # Remove duplicated rows
    df = df.drop_duplicates()

    # Remove rows with invalid values
    for key in df_schema.keys():
        if df_schema[key] == 'int':
            df = df[pd.to_numeric(df[key], errors='coerce').notnull()]
        elif df_schema[key] == 'datetime64[ns, UTC]':
            df = df[pd.to_datetime(df[key], unit='ns', errors='coerce').notnull()]

    # Cast to expected schema
    for col in df_schema.keys():
        if df_schema[col] == 'int':
            df = df.astype({col: 'float64'}).astype({col: 'int'})
        else:
            df = df.astype({col: df_schema[col]})

    return df
