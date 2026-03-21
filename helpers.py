import json
import logging
from requests_cache import CachedSession
from datetime import timedelta

logger = logging.getLogger(__name__)

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace


"""Cached session settings"""
requests_cache_session = CachedSession(
    cache_name="app/cache/local_cache",
    expire_after=timedelta(weeks=12),    # Otherwise expire responses after three months
    allowable_codes=[200, 400],        # Cache 400 responses as a solemn reminder of your failures
    allowable_methods=['GET', 'POST'], # Cache whatever HTTP methods you want
    ignored_parameters=['api_key','X-RapidAPI-Key']  # Don't match this request param, and redact if from the cache
    )
def convert_json(json_str):
    try:
        json_data = json.loads(json_str, strict=False)
        return json_data
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        return None

def Json2Object(json_text):
    """Convert JSON to a JSON object"""
    return json.loads(json_text, object_hook=lambda d: Namespace(**d))

def Object2Json(obj):
    """Convert a JSON object to JSON text"""
    if isinstance(obj, Namespace):
        obj = vars(obj)
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)


def get_data(url: str, headers: dict, params: dict = None):
    """Call an API and return a JSON object from the given url, headers and params — served from cache or live."""
    response = requests_cache_session.get(url, headers=headers, params=params)
    if not response.ok:
        logger.error(f"API error {response.status_code} for {url} | params={params}")
        return None
    try:
        return Json2Object(response.text)
    except Exception as e:
        logger.error(f"Failed to parse API response from {url} | params={params} | error: {e}")
        return None

