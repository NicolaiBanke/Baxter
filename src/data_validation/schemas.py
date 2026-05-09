import pandera.pandas as pa
from pandera.typing import Series, Index


class PriceDataSchema(pa.DataFrameModel):
    Open: Series[float] = pa.Field(gt=0.0, coerce=True)
    High: Series[float] = pa.Field(gt=0.0, coerce=True)
    Low: Series[float] = pa.Field(gt=0.0, coerce=True)
    Close: Series[float] = pa.Field(gt=0.0, coerce=True)
    Volume: Series[int] = pa.Field(ge=0, coerce=True)
    Date: Index[pa.Timestamp] = pa.Field(coerce=True)
