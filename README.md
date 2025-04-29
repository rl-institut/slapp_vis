# Installation

With uv:

```shell
uv venv .venv
source ./.venv/bin/activate
uv snyc
```

In order to compile chart HTMLs:
1. Create folder `dist`
2. Run `python charts.py`
3. Now you should be able to see and visit all charts from dist folder (you can "run" them using PyCharm as well)
