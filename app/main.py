# Простой вариант проверки на анаграммность через sorted(), но учитывая тот факт, что сортировка обычно имеет O(n^2)
# или  O(nlogn), то для более быстрого решения со сложностью O(n) лучше использовать Counter (from collections)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from uvicorn import run
from collections import Counter
from random import sample

from connections import redis_conn, pg_conn
from rand_device import device


app = FastAPI()


@app.on_event('startup')
async def startup_event():
    await redis_conn.init_cache()
    await pg_conn.init_conn()


@app.on_event('shutdown')
async def shutdown_event():
    redis_conn.close()
    await redis_conn.wait_closed()
    await pg_conn.close()


@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse('static/index.html')


@app.get("/anagrams/", tags=['redis'])
async def anagrams(string_1: str, string_2: str):
    def get_counter(s):
        return Counter(s.replace(" ", "").lower())

    result_check = get_counter(string_1) == get_counter(string_2)
    if result_check:
        await redis_conn.incr('counter')

    return {"is_anagrams": result_check,
            "anagrams_count": await redis_conn.get('counter')}


@app.get("/devices/", tags=['pg'])
async def get_devices():
    await pg_conn.execute('SELECT d.dev_type, COUNT(d.dev_type) FROM devices d '
                          'LEFT JOIN endpoints e ON d.id = e.device_id '
                          'WHERE e.id IS NULL GROUP BY d.dev_type')
    res = await pg_conn.cur.fetchall()
    return dict(res)


@app.post("/devices/", status_code=201, tags=['pg'])
async def add_devices(count: int):
    # Т.к. добавлена возможность внесения любого кол-ва устройств, то исходя из условия задачи,
    # что нужно добавить 10 и привязать 5, будем привязывать 1/2 от count (целочисленное деление)
    device_ids = []
    for dev in device(count):
        await pg_conn.execute(f"INSERT INTO devices (dev_id, dev_type) "
                              f"VALUES ('{dev.dev_id}', '{dev.dev_type}') "
                              f"RETURNING id;")
        res_id = await pg_conn.cur.fetchone()
        device_ids.append(res_id[0])

    for dev_id in sample(device_ids, count // 2):
        res = await pg_conn.execute(f"INSERT INTO endpoints (device_id, comment) "
                                    f"VALUES ({dev_id}, 'comment_of_dev_with_id_{dev_id}');")


if __name__ == '__main__':
    run("main:app", port=3000, reload=True)
