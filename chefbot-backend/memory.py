memory = {}

def save_memory(user_id, data):
    if user_id not in memory:
        memory[user_id] = {
            "diet": None,
            "cuisine": None,
            "preferences": [],
            "history": []
        }

    if data.get("diet"):
        memory[user_id]["diet"] = data["diet"]

    if data.get("cuisine") and data["cuisine"] != "none":
        memory[user_id]["cuisine"] = data["cuisine"]

    for p in data.get("preferences", []):
        if p not in memory[user_id]["preferences"]:
            memory[user_id]["preferences"].append(p)

    memory[user_id]["history"].append(data.get("query"))


def get_memory(user_id):
    return memory.get(user_id, {
        "diet": None,
        "cuisine": None,
        "preferences": [],
        "history": []
    })