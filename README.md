# CS2 Tournament Match Site 🎮

A clean, lightweight, and modern web application designed to track and display CS2 Aussie Laozi Cup tournament match results, powered by static hosting and dynamic JSON data rendering.

---

## 🚀 Current Features

- **Dynamic Data Rendering:** Match results and stats are decoupled into an external `matches.json` file and dynamically loaded via JavaScript, making data updates clean and modular.
- **Optimized Project Architecture:** Standardized flat frontend directory layout designed specifically for seamless GitHub Pages deployment without nested routing errors.
- **Zero-Dependency Frontend:** Built using pure HTML5, modern CSS, and Vanilla JavaScript for lightning-fast load times and easy maintenance.
- **Match Detail Pages:** Each match has a detail link. Matches synchronized from FACEIT include team rosters and player statistics.
- **Live Deployment:** Automatically deployed and publicly accessible via GitHub Pages.

---

## 📁 Project Structure

```text
cs2MatchSite/
├── 📄 index.html      # Main entry point of the website
├── 📄 match.html      # Match detail page
├── 📄 match.js        # Match detail rendering logic
├── 📄 style.css       # Custom styling and layout design
├── 📄 script.js       # Dynamic DOM rendering and data fetching logic
├── 📄 matches.json    # Structured match results dataset
└── 📄 README.md       # Project documentation
```

---

## 🔮 Roadmap / Next Development Steps

- [ ] **FACEIT API Integration:** Develop a Python automation script (`update_matches.py`) to fetch real-time match stats and histories directly from the FACEIT API.
- [ ] **Automated Data Pipeline:** Set up automated sync so match results automatically overwrite and update `matches.json`.
- [ ] **UI/UX Enhancement:** Add responsive grid layouts, filtering options (by map, player, or outcome), and team badges.
- [ ] **Leaderboard & Statistics:** Implement aggregate player statistics (K/D ratios, win rates, headshot percentages).

---

## 🛠️ Local Development & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/ivtwWw/Cs2TournamentProject.git
   ```
2. Open the project folder in **VS Code**.
3. Use **Live Server** to preview the site locally.

## FACEIT 数据同步配置

`faceit_sync.py` 不会在源代码中保存 API Key。运行脚本前，请在当前终端会话中设置
`FACEIT_API_KEY` 环境变量：

### Windows PowerShell

```powershell
$env:FACEIT_API_KEY = "你的新 FACEIT API Key"
python faceit_sync.py
```

### Windows 命令提示符

```cmd
set FACEIT_API_KEY=你的新 FACEIT API Key
python faceit_sync.py
```

如果旧 API Key 曾经提交到 Git 或公开仓库，请立即在 FACEIT 开发者后台撤销它并生成新 Key。
不要把新 Key 写入代码、`matches.json`、README 或提交到仓库。

### 同步 BO3

运行 `faceit_sync.py` 后选择 `3=BO3`，然后依次输入 2 或 3 张地图对应的 FACEIT Match 链接或 ID，用逗号分隔。脚本会把各图比分和选手数据合并为同一场系列赛；详情页提供“总览”和逐地图切换。

如果 FACEIT 的系列赛 Match ID 返回了多张地图统计，也可以选择单场同步，脚本会按返回的地图数据生成逐图视图。旧记录若没有地图/选手数据，需要用对应 FACEIT Match ID 重新同步。