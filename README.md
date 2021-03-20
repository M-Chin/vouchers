## Table of Contents
* [How to start pipeline and API](#How to start pipeline and API)
* [Unit Tests](#Unit tests)
* [Data Analysis](#Data Analysis)
* [Customisation](#Customisation)

## How to start pipeline and API
* Build image and start container with it
````
docker build -t voucher .
docker run -p 5000:5000 --name VoucherAPI voucher
````
* Pipeline is triggered and the API is started afterwards. APIs endpoint is:
http://0.0.0.0:5000/voucher

* API curl request example
```
curl --request GET 'http://0.0.0.0:5000/voucher' \
--header 'Content-Type: application/json' \
--data-raw '{
"customer_id": 9999,
"country_code": "Peru",
"last_order_ts": "2021-01-03 00:00:00",
"first_order_ts": "2020-12-03 00:00:00", 
"total_orders": 2,
"segment_name": "frequent_segment"
}'
```

## Unit tests
* From the project's root switch to pipenv environment:
```
pipenv shell
```
* Run unit tests:
```
pytest -v
```                                                           
* Output looks like this:
```
unit_tests/test_segments.py::test_get_frequent_segment PASSED               [ 20%]
unit_tests/test_segments.py::test_get_recency_segment PASSED                [ 40%]
unit_tests/test_segments.py::test_clean_up_data_set PASSED                  [ 60%]
unit_tests/test_segments.py::test_get_most_used_voucher_per_segment PASSED  [ 80%]
unit_tests/test_segments.py::test_build_segments PASSED                     [100%]
```
## Data Analysis
Check `Data Analysis.pdf`

## Customisation
#### Tune segments
`modules/segment_definitions.py`

The segment's definitions can be tuned here, either changing the intervals or changing the name variants.
#### Adding more countries
`modules/generate_segments.py`

More countries can be activated by changing the variable ACTIVE_COUNTRIES,
e.g.

```ACTIVE_COUNTRIES = ['China', 'Peru', 'Australia', 'Latvia']```