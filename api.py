from datetime import datetime
import flask
from flask import Flask
import json
from jsonschema import validate

from modules.segment_definitions import get_recency_segment, get_frequent_segment
from modules.generate_segments import SegmentVouchers

app = Flask(__name__)

voucher_values = SegmentVouchers()

# Expected JSON from api request
SCHEMA = {
    "type": "object",
    "properties": {
        "customer_id": {"type": "number"},
        "country_code": {"type": "string"},
        "last_order_ts": {"type": "string"},
        "first_order_ts": {"type": "string"},
        "total_orders": {"type": "number"},
        "segment_name": {"type": "string"},
    },
}


# Assign a segment to the requested user
def get_segment_variant(json_data):
    segment_var = ''

    if json_data['segment_name'] == 'frequent_segment':
        segment_var = get_frequent_segment(json_data['total_orders'])
    elif json_data['segment_name'] == 'recency_segment':
        days = (datetime.utcnow() - datetime.strptime(
            json_data['last_order_ts'], '%Y-%m-%d %H:%M:%S')).days
        segment_var = get_recency_segment(days)

    return segment_var


@app.route('/voucher', methods=["GET"])
def voucher():
    json_data = flask.request.json

    # Validate json
    validate(instance=json_data, schema=SCHEMA)

    # Check if it's a valid country
    if json_data['country_code'] in voucher_values.get_voucher_values().keys():

        # Get segment variant for requested customer
        segment_var = get_segment_variant(json_data)

        # Get possible vouchers for segment
        vouchers = voucher_values.get_voucher_values()[json_data['country_code']][json_data['segment_name']] \
            .to_dict('records')

        # Returns voucher amount for segment variant
        for i in vouchers:
            if i[json_data['segment_name']] == segment_var:
                return json.dumps({'voucher_amount': i['voucher_amount']})

    return 'No segment found'


if __name__ == '__main__':
    # Run pipeline to generate segments
    voucher_values.generate_segments()
    # Run API
    app.run(host="0.0.0.0", port=5000)
