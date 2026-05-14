from pandera import check_types
from pathlib import Path
from .schemas import PriceDataSchema
import pandas as pd
from pandera.typing import DataFrame


@check_types
def get_validated_data(hdf5_dir: Path, ticker: str) -> DataFrame[PriceDataSchema]:
    with pd.HDFStore(hdf5_dir) as store:
        data: DataFrame = store.get(f"price_series/{ticker}")  # ty: ignore
    return data
