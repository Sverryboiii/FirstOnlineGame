from src.server import data, file_manager

async def parse_payload(payload: dict) -> dict | None:
    return await operations.get(payload.get("op", 0), operations[0])(payload)

async def register_user(payload) -> dict:
    user = file_manager.register_user(payload.get("UN", f"player{data.UID}"), payload.get("PW", None))
    if user.get("STATUS", 0) == 0:
        return {"STATUS": 0}
    data.users[data.SESSION_ID] = user.get("player")
    print(f"Player {data.UID} connected with session ID {data.SESSION_ID}!")
    return {"UID": data.SESSION_ID, "STATUS": 1}

async def key(payload) -> None:
    user = data.users[payload.get("UID", 0)]
    k = payload.get("KEYS", [])
    if "a" in k:
        user.x -= 1
    if "d" in k:
        user.x += 1
    if "w" in k:
        user.y -= 1
    if "s" in k:
        user.y += 1

    return None

async def request_draw_info(_) -> dict:

    draw_info = {
        'players': []
    }

    for p in data.users.values():
        draw_info['players'].append((p.x, p.y))

    return draw_info

async def log_off(payload: dict) -> None | dict:
    if not payload.get("UID"):
        return {
            "STATUS": 0
        }

    try:
        file_manager.save_user(_player=data.users[payload["UID"]])
        data.users.pop(payload.get("UID", 0))
        print(
            f"Player {payload.get('UID', 0)} disconnected!",
            f"There are now {len(data.users)} players online."
        )
    except KeyError:
        print(f"User {payload.get('UID', 0)} tried to disconnect, but failed!")
    return None

operations = {
    0: lambda x : None,
    1: register_user,
    2: key,
    3: request_draw_info,
    4: log_off
}