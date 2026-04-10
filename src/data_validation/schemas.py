import pandera as pa
from pandera.typing import Series


class PriceDataSchema(pa.DataFrameModel):
    Open: Series[float] = pa.Field(gt=0.0, coerce=True)
    High: Series[float] = pa.Field(gt=0.0, coerce=True)
    Low: Series[float] = pa.Field(gt=0.0, coerce=True)
    Close: Series[float] = pa.Field(gt=0.0, coerce=True)
    Volume: Series[int] = pa.Field(ge=0, coerce=True)
