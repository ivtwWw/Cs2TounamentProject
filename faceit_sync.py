import json
import os
import re

import requests


FACEIT_API_KEY_ENV = "FACEIT_API_KEY"
JSON_FILE = "matches.json"


def parse_player_stats(stats_data, factions):
    """将 FACEIT stats 接口的队伍/选手数据转换为前端使用的结构。"""
    rounds = stats_data.get("rounds", [])
    if not rounds:
        return []

    round_data = rounds[0]
    teams_data = round_data.get("teams", [])
    if isinstance(teams_data, dict):
        teams_data = list(teams_data.values())

    result = []
    for team_data in teams_data:
        team_id = team_data.get("team_id") or team_data.get("faction_id")
        team_name = next(
            (
                faction.get("name")
                for faction in factions
                if faction.get("faction_id") == team_id
            ),
            team_data.get("team_name", "未知队伍"),
        )
        players = []
        for player in team_data.get("players", []):
            player_stats = player.get("player_stats", {})
            players.append(
                {
                    "nickname": player.get("nickname", "未知选手"),
                    "playerId": player.get("player_id"),
                    "stats": player_stats,
                }
            )
        result.append({"name": team_name, "players": players})
    return result


def extract_match_id(url_or_id):
    """从 FACEIT 房间链接中提取纯净的 Match ID"""
    match = re.search(r"room/([a-zA-Z0-9-]+)", url_or_id)
    if match:
        return match.group(1)
    return url_or_id.strip()


def fetch_faceit_match(match_id):
    """调用 FACEIT OpenAPI 抓取比赛数据和统计结果"""
    api_key = os.environ.get(FACEIT_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"未设置 {FACEIT_API_KEY_ENV} 环境变量。"
            "请先配置 FACEIT API Key，再运行同步脚本。"
        )

    headers = {"Authorization": "Bearer " + api_key}
    base_url = f"https://open.faceit.com/data/v4/matches/{match_id}"
    stats_url = f"https://open.faceit.com/data/v4/matches/{match_id}/stats"

    print(f"\n⏳ 正在向 FACEIT 请求比赛数据 (Match ID: {match_id})...")

    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ 获取基础信息失败！HTTP 状态码: {response.status_code}")
        return None

    data = response.json()
    try:
        faction1 = data["teams"]["faction1"]
        faction2 = data["teams"]["faction2"]
        factions = [faction1, faction2]
        team_a = faction1["name"]
        team_b = faction2["name"]

        voting = data.get("voting", {})
        map_name = "未知地图"
        if voting and "map" in voting and "pick" in voting["map"]:
            map_name = voting["map"]["pick"][0]

        stats_resp = requests.get(stats_url, headers=headers)
        score = "未出结果"
        winner = "待定"
        details = {"teams": []}

        if stats_resp.status_code == 200:
            stats_data = stats_resp.json()
            details["teams"] = parse_player_stats(stats_data, factions)
            if "rounds" in stats_data and len(stats_data["rounds"]) > 0:
                match_stats = stats_data["rounds"][0]["round_stats"]
                raw_score = match_stats.get("Score", "0 / 0")
                score = raw_score.replace("/", "-").strip()

                winner_id = match_stats.get("Winner")
                if winner_id == faction1["faction_id"]:
                    winner = team_a
                elif winner_id == faction2["faction_id"]:
                    winner = team_b
                else:
                    winner = "无法解析胜者"
        else:
            print("⚠️ 警告：统计数据尚未生成，如果比赛刚刚结束，请等待几分钟后重试。")

        print("✅ 抓取成功！\n")
        return {
            "id": match_id,
            "faceitUrl": f"https://www.faceit.com/en/cs2/room/{match_id}",
            "stage": "新比赛 (需手动修改阶段名称)",
            "info": f"地图: {map_name}",
            "teamA": team_a,
            "teamB": team_b,
            "score": score,
            "winner": winner,
            "details": details,
        }
    except Exception as error:
        print(f"❌ 解析比赛数据时发生错误: {error}")
        return None


def main():
    print("========================================")
    print("🏆 Aussie Laozi Cup 战绩半自动同步工具")
    print("========================================")

    if not os.environ.get(FACEIT_API_KEY_ENV):
        print(
            f"❌ 未设置 {FACEIT_API_KEY_ENV} 环境变量。"
            "请先配置 FACEIT API Key！"
        )
        return

    user_input = input("\n请粘贴 FACEIT 比赛链接 或 直接输入 Match ID：\n> ")
    match_id = extract_match_id(user_input)

    match_data = fetch_faceit_match(match_id)
    if not match_data:
        return

    print("-" * 40)
    print("获取到的比赛数据如下：")
    print(f"对阵: {match_data['teamA']} VS {match_data['teamB']}")
    print(f"地图: {match_data['info']}")
    print(f"比分: {match_data['score']}")
    print(f"胜者: {match_data['winner']}")
    print("-" * 40)

    confirm = input("数据是否准确？(y/N, 输入 n 可以丢弃并手动修正): ").strip().lower()

    if confirm == "y":
        stage = input(
            "请输入这是哪场比赛 (例如 '半决赛 (BO1)' 或 'S4常规赛'): "
        ).strip()
        if stage:
            match_data["stage"] = stage

        data_store = {"matches": []}
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                try:
                    data_store = json.load(file)
                except json.JSONDecodeError:
                    pass

        data_store["matches"].insert(0, match_data)

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(data_store, file, ensure_ascii=False, indent=2)

        print(
            f"\n🎉 成功！已将 {match_data['teamA']} VS "
            f"{match_data['teamB']} 的战绩写入 {JSON_FILE}。"
        )
        print("现在你可以执行 `git add .` -> `git commit` -> `git push` 发布最新战绩了！")
    else:
        print("已取消保存，如果因为重赛导致 API 数据错误，建议直接手动修改 matches.json。")


if __name__ == "__main__":
    main()
