from typing import Optional

import geopandas
import pandas as pd
from handler_app import plh
from pydantic import BaseModel
from responses import GpkgFileResponse


class FunModel(BaseModel):
    item_name: str
    item_value: Optional[int]


class ListFunModel(BaseModel):
    __root__: list[FunModel]


@plh.get("/response_model", response_model=FunModel)
def response_model(secret):
    return {"item_name": secret}


@plh.get("/list_response")
def response_list():
    return [{"item_name": 1}]


@plh.get("/list_response_model", response_model=ListFunModel)
def response_list_model():
    """List models"""
    return [{"item_name": "secret"}]


@plh.get("/response_file", response_class=GpkgFileResponse)
def response_model(secret):
    df = pd.DataFrame(
        {
            "City": ["Buenos Aires", "Brasilia", "Santiago", "Bogota", "Caracas"],
            "Country": ["Argentina", "Brazil", "Chile", "Colombia", "Venezuela"],
            "Latitude": [-34.58, -15.78, -33.45, 4.60, 10.48],
            "Longitude": [-58.66, -47.91, -70.66, -74.08, -66.86],
        }
    )

    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))

    file = gdf.to_file("package.gpkg", layer="countries", driver="GPKG")
    return GpkgFileResponse(file)
