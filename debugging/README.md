# Debugging Demo
You can find our debugging guide here: https://vector.dev/guides/developer/debugging/

## Debug Server Usage
```sh
python3 fake_server.py
```

```sh
# Change server response status to always be 404
curl -X POST http://localhost:8000/set_status -H "Content-Type: application/json" -d '{"status": 404}'
# Revert to always return 200
curl -X POST http://localhost:8000/set_status -H "Content-Type: application/json" -d '{"status": 200}'
```
