def get_frequent_segment(total_orders):
    if 0 <= total_orders <= 4:
        segment = '0-4'
    elif 5 <= total_orders <= 13:
        segment = '5-13'
    elif 14 <= total_orders <= 37:
        segment = '13-37'
    else:
        segment = 'no_segment'
    return segment


def get_recency_segment(days_since_order):
    if 30 <= days_since_order <= 60:
        segment = '30-60'
    elif 61 <= days_since_order <= 90:
        segment = '60-90'
    elif 91 <= days_since_order <= 120:
        segment = '90-120'
    elif 121 <= days_since_order <= 180:
        segment = '120-180'
    elif 181 <= days_since_order:
        segment = '180+'
    else:
        segment = 'no_segment'
    return segment


# Adds additional columns to help determine a segment
def add_additional_columns(df):
    # Generate days_since_order column for recency segment
    df['days_since_order'] = (df['timestamp'] - df['last_order_ts']).dt.days
    return df
