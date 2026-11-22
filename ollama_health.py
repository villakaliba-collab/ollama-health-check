#!/usr/bin/env python3
"""Ollama Health Check - Simple local AI server monitor."""

import json
import sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

BASE_URL = "http://127.0.0.1:11434"
TIMEOUT = 3


def request(path):
    with urlopen(BASE_URL + path, timeout=TIMEOUT) as response:
        return json.load(response)


def main():
    print("Ollama Health Check")
    print("-------------------")

    try:
        version = request("/api/version")
        data = request("/api/tags")

        models = data.get("models", [])

        print("Status: ONLINE")
        print("Version:", version.get("version", "Unknown"))
        print("Installed models:", len(models))

        for model in models:
            print(" -", model.get("name", "Unknown"))

        return 0

    except (URLError, HTTPError, TimeoutError, OSError,
            ValueError, KeyError, TypeError) as error:
        print("Status: OFFLINE or unavailable")
        print("Error:", error)
        return 1


if __name__ == "__main__":
    sys.exit(main())
