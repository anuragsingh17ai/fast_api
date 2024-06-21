from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get('/items/')
async def read_items(q: Annotated[str | None, Query(min_length=10,max_length=50, pattern='^fixedquery$')] = None):
    results = {'items': [{'item_id':'Foo'},{'item_id':'Bar'}]}

    if q:
        results.update({'q':q})
    return results


@app.get('')   # http://localhost:8000/items/?q=foo&q=bar
async def read_items(q: Annotated[list[str] | None,Query()]=None):
    query_items = {'q':q}
    return query_items