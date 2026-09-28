import json
import os
import tempfile

from tools.faceit_sync import (
    JSON_FILE,
    combine_bo3_matches,
    extract_match_id,
    fetch_faceit_match,
)


def load_store():
    if not JSON_FILE.exists():
        raise FileNotFoundError(f"找不到比赛数据文件：{JSON_FILE}")

    with JSON_FILE.open("r", encoding="utf-8") as file:
        store = json.load(file)
    if not isinstance(store, dict) or not isinstance(store.get("matches"), list):
        raise ValueError(f"比赛数据文件格式错误：{JSON_FILE}")
    return store


def save_store(store):
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=JSON_FILE.parent,
            delete=False,
            suffix=".tmp",
        ) as file:
            json.dump(store, file, ensure_ascii=False, indent=2)
            file.write("\n")
            temporary_path = file.name
        os.replace(temporary_path, JSON_FILE)
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)


def display_matches(matches):
    if not matches:
        print("\n目前没有比赛记录。")
        return

    print("\n当前比赛：")
    for index, match in enumerate(matches, start=1):
        print(
            f"{index}. [{match.get('stage', '未命名赛事')}] "
            f"{match.get('teamA', '未知队伍')} {match.get('score', '-')} "
            f"{match.get('teamB', '未知队伍')} "
            f"({match.get('format', '未标注赛制')})"
        )


def remove_match():
    store = load_store()
    matches = store["matches"]
    display_matches(matches)
    if not matches:
        return

    selection = input("\n输入要删除的比赛编号，输入 0 返回：").strip()
    if selection == "0":
        return
    if not selection.isdigit() or not 1 <= int(selection) <= len(matches):
        print("编号无效，没有删除任何比赛。")
        return

    index = int(selection) - 1
    match = matches[index]
    print(
        f"\n即将删除：{match.get('stage', '未命名赛事')} | "
        f"{match.get('teamA', '?')} {match.get('score', '-')} "
        f"{match.get('teamB', '?')}"
    )
    if input("确认删除？此操作会立即修改本地数据文件 (y/N)：").strip().lower() != "y":
        print("已取消，比赛记录未更改。")
        return

    del matches[index]
    save_store(store)
    print(f"已删除比赛；更新文件：{JSON_FILE}")


def collect_map_match(match_id):
    match = fetch_faceit_match(extract_match_id(match_id))
    if match is None:
        raise RuntimeError("无法获取这场 FACEIT 比赛。")
    return match


def add_match():
    if not os.environ.get("FACEIT_API_KEY"):
        print("请先设置 FACEIT_API_KEY 环境变量，再录入 FACEIT 比赛。")
        return

    match_type = input(
        "录入方式：1=单个 FACEIT 链接（自动识别 BO1/BO3），"
        "3=多个地图链接手动合并为 BO3："
    ).strip()
    if match_type == "1":
        match_url = input("粘贴 FACEIT 比赛链接或 Match ID：").strip()
        new_match = collect_map_match(match_url)
    elif match_type == "3":
        raw_ids = input(
            "按地图顺序输入 2 或 3 个 FACEIT 链接/Match ID，用逗号分隔："
        )
        ids = [item.strip() for item in raw_ids.split(",") if item.strip()]
        if len(ids) not in (2, 3):
            print("BO3 需要输入 2 或 3 场地图比赛。没有录入数据。")
            return

        map_matches = []
        for match_id in ids:
            try:
                map_matches.append(collect_map_match(match_id))
            except (RuntimeError, ValueError) as error:
                print(f"录入失败：{error} 未写入任何数据。")
                return
        new_match = combine_bo3_matches(map_matches)
    else:
        print("类型无效，没有录入数据。")
        return

    new_match["stage"] = input("请输入赛事阶段/名称：").strip() or "新比赛"
    print(
        f"\n待添加：{new_match['stage']} | {new_match['teamA']} "
        f"{new_match['score']} {new_match['teamB']} "
        f"({new_match.get('format', 'BO1')})"
    )
    if input("确认添加到比赛列表？(y/N)：").strip().lower() != "y":
        print("已取消，比赛记录未更改。")
        return

    store = load_store()
    existing_ids = {match.get("id") for match in store["matches"]}
    if new_match.get("id") in existing_ids:
        print("这场比赛已存在（Match ID 重复），未添加。")
        return
    store["matches"].insert(0, new_match)
    save_store(store)
    print(f"已添加比赛；更新文件：{JSON_FILE}")


def main():
    while True:
        print(
            "\n========== CS2 比赛数据管理 ==========\n"
            "1. 查看比赛列表\n"
            "2. 拉取并添加新比赛\n"
            "3. 删除比赛\n"
            "0. 退出"
        )
        choice = input("请选择：").strip()

        try:
            if choice == "1":
                display_matches(load_store()["matches"])
            elif choice == "2":
                add_match()
            elif choice == "3":
                remove_match()
            elif choice == "0":
                print("已退出。")
                return
            else:
                print("选项无效，请重新输入。")
        except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as error:
            print(f"操作失败：{error}")


if __name__ == "__main__":
    main()
