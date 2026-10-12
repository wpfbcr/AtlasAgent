"""Bounded JSON requests shared by AtlasAgent's public API clients."""
import json
import time
import urllib.error
import urllib.request


class APIError(RuntimeError):
    pass


def fetch_json(url, timeout=5, retries=2):
    request = urllib.request.Request(url, headers={"User-Agent": "AtlasAgent/1.2"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
            if not isinstance(data, dict):
                raise APIError("Service returned a non-object JSON response")
            if data.get("error"):
                raise APIError(str(data.get("reason", "Service rejected the request")))
            return data
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == retries:
                raise APIError("Service HTTP error {}".format(exc.code)) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt == retries:
                raise APIError("Service unavailable after {} attempts: {}".format(attempt + 1, exc)) from exc
        except (ValueError, UnicodeError) as exc:
            raise APIError("Service returned invalid JSON") from exc
        time.sleep(0.2 * (attempt + 1))
    raise APIError("Service unavailable")
