import aiohttp
import pytest


@pytest.mark.skip(reason="no valid saxo api key")
@pytest.mark.asyncio
async def test_execute_order(saxo_execution_handler, mkt_order):
    async with aiohttp.ClientSession(
        base_url=saxo_execution_handler.base_url, headers=saxo_execution_handler.headers
    ) as session:
        res = await saxo_execution_handler.execute_order(mkt_order, session=session)
    assert res.status == 200
