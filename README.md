<div align="center">
<h1>pyJPI</h1>
<p>An asynchronous Python module to interact with Android devices running JPI.</p>
</div>

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/trychlos/pyjpi)

<!--
[![CodeRabbit.ai is Awesome](https://img.shields.io/badge/AI-orange?label=CodeRabbit&color=orange&link=https%3A%2F%2Fcoderabbit.ai)](https://coderabbit.ai)
[![renovate maintained](https://img.shields.io/badge/maintained%20with-renovate-blue?logo=renovatebot)](https://github.com/compatech/python-airos/issues/8)

[![PyPI version fury.io](https://badge.fury.io/py/airos.svg)](https://pypi.python.org/pypi/airos/)
[![Latest release](https://github.com/compatech/python-airos/workflows/Latest%20release/badge.svg)](https://github.com/compatech/python-airos/actions)
[![Newest commit](https://github.com/compatech/python-airos/workflows/Latest%20commit/badge.svg)](https://github.com/compatech/python-airos/actions)

[![CodeFactor](https://www.codefactor.io/repository/github/compatech/python-airos/badge)](https://www.codefactor.io/repository/github/plugwise/python-airos)
[![codecov](https://codecov.io/gh/compatech/python-airos/graph/badge.svg?token=WI5K2IZWNS)](https://codecov.io/gh/compatech/python-airos)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=CoMPaTech_python-airos&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=CoMPaTech_python-airos)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=CoMPaTech_python-airos&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=CoMPaTech_python-airos)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=CoMPaTech_python-airos&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=CoMPaTech_python-airos)
-->

# Overview

`pyJPI` is an asynchronous Python library designed to programmatically interact with Android devices running JPI.

This library is a key component for an in-the-way potential future core integration with [Home Assistant](https://www.home-assistant.io).

More details on the integration can be found on the [JPI](https://www.home-assistant.io/integrations/jpi/) page. To add JPI directly feel free to use the button below:

[![Open your Home Assistant instance and show your integrations.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/_change/?redirect=config_flow_start%2F%3Fdomain%3Djpi)

## Features

- Asynchronous operations are built with ``aiohttp` for non-blocking I/O, which is perfect for integrations and background tasks.
- API: `battInfo`
- API: `getDeviceName`

## Installation

You can install `pyJPI` from PyPI using pip:

```Bash
pip install pyjpi
```

## Usage

Here is a more detailed example of how to use the library to connect, fetch status, and perform an action on an Android device running JPI.

```Python
import aiohttp
from pyjpi import jpiInit

async def main():
    """Main function to demonstrate library usage."""
    # Create an aiohttp session with SSL verification disabled.
    # Be cautious with this setting; it's useful for self-signed certificates
    # but not recommended for production environments without proper validation.
    session = aiohttp.ClientSession( connector=aiohttp.TCPConnector( verify_ssl=False ))

    # Get a handle on the pyJPI library.
    handle = await jpiInit( session )

    # Have an URL somewhere.
    url = "http://myhost.example.com:8080"

    # Then just has to call the library functions.
    try:
        res = await handle.get( url )
        # returns an object { resp: ClientResponse, text: str } or False
        res = await handle.getDeviceName( url )
        # returns the device name as set by the manufacturer (a single string) or False
        res = await handle.battInfo( url )
        # returns an object { level: integer, charging: bool, power: bool }


if __name__ == "__main__":
    main()
```

## Available functions

- `async jpiInit( session: aiohttp.ClientSession ) -> JPILibrary`:

Initializes the library.

Returns a handle on it.

## Available classes

- `JPILibrary`:

The class which manages the devices accesses.

## Avaliable `JPILibrary` method

- `async get( url: str) -> dict`:

Runs a HTTP GET method on the specified URL.

Returns a dict with:

    - resp: the `aiohttp.ClientResponse`
    - text: the resp.text() content

- `async getDeviceName( url: str) -> str`:

Runs a HTTP GET method on f"{url}?action=getDeviceName" url.

Returns a string which contains the device name as set by the manufacturer.

- `async battInfo( url: str) -> dict`:

Runs a HTTP GET method on on f"{url}?action=battInfo" url.

Returns a dict with:

    - level: an integer with the current battery level in %
    - charging: a boolean which says if the battery is currently charging
    - power: a boolean which says if the power is on on the device.

## Contributing

We welcome contributions as well as additional codeowners to pyjpi.

## Issues & help

In case of support or error, please report your issue request to our [Issues tracker](https://github.com/trychlos/pyjpi/issues).
