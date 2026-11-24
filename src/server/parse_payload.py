from src.server import data, file_manager

def parse_payload(payload: dict) -> bytes | None:
    return operations.get(payload.get("op", 0), operations[0])(payload)

def register_user(payload) -> bytes:
    user = file_manager.register_user(payload.get("UN", f"player{data.UID}"), payload.get("PW", None))
    data.users[data.UID] = user["player"]
    print(f"Player {data.UID} connected with session ID {data.SESSION_ID}!")
    return {"UID": data.SESSION_ID, "STATUS": 1} if user["STATUS"] else {"STATUS": 0}

def connect_user(payload) -> bytes:
    user = file_manager.connect_user(payload.get("UN"), payload.get("PW"))
    data.users[data.UID] = user["player"]
    print(f"Player {data.UID} connected with session ID {data.SESSION_ID}!")
    return {"UID": data.SESSION_ID, "STATUS": 1} if user["STATUS"] else {"STATUS": 0}

def key(payload) -> None:
    user = data.users[payload.get("UID", 0)]
    k = payload.get("KEYS", [])
    if "a" in k:
        user.x -= 1
    elif "d" in k:
        user.x += 1
    elif "w" in k:
        user.y -= 1
    elif "s" in k:
        user.y += 1

    return None

def request_draw_info(_) -> bytes:

    draw_info = {
        'players': []
    }

    for p in data.users.values():
        draw_info['players'].append((p.x, p.y))

    return draw_info

def log_off(payload: dict) -> None:

    try:
        data.users.pop(payload.get("UID", 0))
        print(f"Player {payload.get('UID', 0)} disconnected!")
        print(f"There are now {len(data.users)} players online.")
    except KeyError:
        print(f"User {payload.get('UID', 0)} tried to disconnect, but failed!")
    return None

operations = {
    0: lambda x : None,
    1: register_user,
    2: key,
    3: request_draw_info,
    4: log_off,
    5: connect_user
}