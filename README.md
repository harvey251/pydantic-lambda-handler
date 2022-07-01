# Vision

Aim to create an easy to use

```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
def create_item(item: Item):
    return item
```

## MUST HAVE
* creates open api schema