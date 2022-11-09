# ddcrash

## Problem

We are seeing a ddtrace connection timeout when we run our pytest tests even if we explicitly tell pytest/ddtrace not to trace using `-p no:ddtrace -p no:ddtrace.pytest_bdd`.

## Reproduce

```bash
pip install -r requirements.txt
```

Run the following command:

```bash
$ pytest -s -vv -p no:ddtrace -p no:ddtrace.pytest_bdd test_dd.py
```

You should see something like:

```
============================================================ test session starts =============================================================
platform darwin -- Python 3.10.8, pytest-7.2.0, pluggy-1.0.0 -- /Users/fredrik/code/repos/ddcrash/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/fredrik/code/repos/ddcrash
collected 1 item                                                                                                                             

test_dd.py::test_crash PASSED

============================================================= 1 passed in 6.76s ==============================================================
failed to send traces to Datadog Agent at http://localhost:8126/v0.4/traces
Traceback (most recent call last):
  File "/Users/fredrik/code/repos/ddcrash/.venv/lib/python3.10/site-packages/tenacity/__init__.py", line 409, in __call__
    result = fn(*args, **kwargs)
  File "/Users/fredrik/code/repos/ddcrash/.venv/lib/python3.10/site-packages/ddtrace/internal/writer.py", line 447, in _send_payload
    response = self._put(payload, headers)
  File "/Users/fredrik/code/repos/ddcrash/.venv/lib/python3.10/site-packages/ddtrace/internal/writer.py", line 399, in _put
    self._conn.request("PUT", self._endpoint, data, headers)
  File "/Users/fredrik/.pyenv/versions/3.10.8/lib/python3.10/http/client.py", line 1282, in request
    self._send_request(method, url, body, headers, encode_chunked)
  File "/Users/fredrik/.pyenv/versions/3.10.8/lib/python3.10/http/client.py", line 1328, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
  File "/Users/fredrik/.pyenv/versions/3.10.8/lib/python3.10/http/client.py", line 1277, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
  File "/Users/fredrik/.pyenv/versions/3.10.8/lib/python3.10/http/client.py", line 1037, in _send_output
    self.send(msg)
  File "/Users/fredrik/.pyenv/versions/3.10.8/lib/python3.10/http/client.py", line 975, in send
    self.connect()
  File "/Users/fredrik/.pyenv/versions/3.10.8/lib/python3.10/http/client.py", line 941, in connect
    self.sock = self._create_connection(
  File "/Users/fredrik/.pyenv/versions/3.10.8/lib/python3.10/socket.py", line 845, in create_connection
    raise err
  File "/Users/fredrik/.pyenv/versions/3.10.8/lib/python3.10/socket.py", line 833, in create_connection
    sock.connect(sa)
ConnectionRefusedError: [Errno 61] Connection refused

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/fredrik/code/repos/ddcrash/.venv/lib/python3.10/site-packages/ddtrace/internal/writer.py", line 564, in flush_queue
    self._retry_upload(self._send_payload, encoded, n_traces)
  File "/Users/fredrik/code/repos/ddcrash/.venv/lib/python3.10/site-packages/tenacity/__init__.py", line 406, in __call__
    do = self.iter(retry_state=retry_state)
  File "/Users/fredrik/code/repos/ddcrash/.venv/lib/python3.10/site-packages/tenacity/__init__.py", line 363, in iter
    raise retry_exc from fut.exception()
tenacity.RetryError: RetryError[<Future at 0x102c4b910 state=finished raised ConnectionRefusedError>]
```

## Workaround

We can run the command with `DD_TRACE_ENABLED=false` and there is no longer a timeout:

```bash
$ DD_TRACE_ENABLED=false pytest -s -vv test_dd.py
```
