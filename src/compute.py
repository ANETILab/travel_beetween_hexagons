import polars as pl
import polars_h3 as plh3
from valhalla import Actor, get_config
from multiprocessing import Pool


def kernel(row, costing: str = "auto") -> list:
    query = {
        "locations": [row["home_latlng"], row["work_latlng"]],
        "costing": costing,
        "radius": 20,
    }
    try:
        temp = actor.optimized_route(query)
    except:
        print((row["source"], row["target"]))
        return [
            row["source"],
            row["target"],
            None,
            None,
        ]

    return [
        row["source"],
        row["target"],
        temp["trip"]["summary"]["length"],
        temp["trip"]["summary"]["time"],
    ]


if __name__ == "__main__":
    COSTING = "auto"
    od = pl.read_csv("../untracked/od.csv")
    od = od.with_columns(
        plh3.cell_to_latlng(pl.col.source).alias("home_latlng"),
        plh3.cell_to_latlng(pl.col.target).alias("work_latlng"),
    ).with_columns(
        pl.struct(
            id=pl.col("source"),
            lat=pl.col("home_latlng").list.get(0).round(7),
            lon=pl.col("home_latlng").list.get(1).round(7),
        ).alias("home_latlng"),
        pl.struct(
            id=pl.col("target"),
            lat=pl.col("work_latlng").list.get(0).round(7),
            lon=pl.col("work_latlng").list.get(1).round(7),
        ).alias("work_latlng"),
    )

    config = get_config(
        tile_extract="../data/valhalla/budapest/valhalla_tiles.tar",
        tile_dir="../data/valhalla/budapest/",
    )

    config["service_limits"]["pedestrian"]["max_matrix_location_pairs"] = (
        len(od) * len(od) * 10
    )

    config["service_limits"]["auto"]["max_matrix_location_pairs"] = (
        len(od) * len(od) * 10
    )
    actor = Actor(config)

    partials = []
    with Pool(8) as p:
        partials = p.map(kernel, od.iter_rows(named=True))

    df = pl.from_records(
        partials, schema=["source", "target", "length", "time"], orient="row"
    )
    df = df.with_columns(pl.lit(COSTING).alias("costing"))
    df.write_csv(f"../output/od_travel_{COSTING}.csv")
