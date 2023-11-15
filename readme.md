exercise 1:
------------ 
curl http://127.0.0.1:5000/ping

exercise 2: 
------------
curl -H "Authorization: Bearer your_secret_key" http://127.0.0.1:5000/ping

exercise 3: 
------------
curl -X POST -H "Content-Type: application/json" -d '{"key": "example_key", "value": "example_value"}' http://127.0.0.1:5000/save
curl 'http://127.0.0.1:5000/get?key=example_key'
curl -X DELETE 'http://127.0.0.1:5000/delete?key=example_key'

exercise 4:
-----------
curl -X POST -H "Content-Type: application/json" -d '{"key": "test_key", "value": "test_value"}' http://127.0.0.1:5000/save
curl 'http://127.0.0.1:5000/get?key=test_key'
curl -X DELETE 'http://127.0.0.1:5000/delete?key=test_key'
