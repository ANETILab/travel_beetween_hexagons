# calculate travel times between hexagons

The administrative boundary of [Budapest](https://en.wikipedia.org/wiki/Budapest) is divided into [H3](https://h3geo.org) hexagons. The centroid of each hexagon is used to represent a starting point. The travel distance and time between starting and ending hexagons are calculated using the [Valhalla routing engine](https://github.com/valhalla/valhalla).

## output

The output has a start (source) and an ending (target) hexagons ID, the route length (in kilometers), the time to take the trip (in seconds) and the costind that can be auto (for car routing) and pedestrian for walking.

For auto costing there might be trips which were cannot be routed, thus the length and the a time is NA.

### sample

| source          | target          | length | time    | costing |
|-----------------|-----------------|--------|---------|---------|
| 891e0363687ffff | 891e0378d8bffff | 6.453  | 452.538 | auto    |
| 891e0379d83ffff | 891e037aa0bffff | 8.79   | 670.64  | auto    |
| 891e037334bffff | 891e0371213ffff | 5.967  | 504.47  | auto    |
| 891e1cb69a3ffff | 891e1cb69b7ffff |        |         | auto    |

## setup

The [`pyproject.toml`](pyproject.toml) document the required dependencies. It's suggested to use the [uv](https://docs.astral.sh/uv/) packaging tool. In this case, just issue the `uv sync` command to set up a virtual environment with all the necessary dependencies.

The script can be run through the uv, using `uv run compute.py`, with the virtualenv set up by uv.

## licensing

The file-level licensing information is described in the REUSE.toml accoding to the [REUSE convention](https://reuse.software/).
