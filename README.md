# CS2 Tournament Match Site 🎮

A clean, lightweight, and modern web application designed to track and display CS2 Aussie Laozi Cup tournament match results, powered by static hosting and dynamic JSON data rendering.

---

## 🚀 Current Features

- **Dynamic Data Rendering:** Match results and stats are stored in `data/matches.json` and loaded dynamically.
- **Organized Project Structure:** Frontend assets, match data, sync tools, and documentation are grouped by purpose. HTML entry pages stay at the repository root for GitHub Pages.
- **Zero-Dependency Frontend:** Built using pure HTML5, modern CSS, and Vanilla JavaScript for lightning-fast load times and easy maintenance.
- **Match Detail Pages:** Each match has a detail link. Matches synchronized from FACEIT include team rosters and player statistics.
- **Live Deployment:** Automatically deployed and publicly accessible via GitHub Pages.

---

## 📁 Project Structure

```text
cs2MatchSite/
├── 📄 .gitignore                 # Local files and generated Python cache exclusions
├── 📁 .vscode/
│   └── 📄 tasks.json             # VS Code workspace tasks
├── 📄 index.html                 # Main page (kept at root for GitHub Pages)
├── 📄 match.html                 # Match detail page
├── 📄 about.html                 # About the community tournament
├── 📁 assets/
│   ├── 📁 css/
│   │   └── 📄 style.css          # Site styles
│   └── 📁 js/
│       ├── 📄 script.js          # Match list rendering
│       └── 📄 match.js           # Match detail rendering
├── 📁 data/
│   └── 📄 matches.json           # Match results and player statistics
├── 📁 tools/
│   ├── 📄 faceit_sync.py         # FACEIT match data sync helpers
│   └── 📄 manage_matches.py      # Local match management menu
├── 📁 docs/
│   └── 📄 changelog.md           # Change history
└── 📄 README.md                  # Project documentation
```

---

## 🔮 Roadmap / Next Development Steps

- [x] **FACEIT API Integration:** Fetch match and player stats from the FACEIT API using `tools/faceit_sync.py`.
- [x] **BO3 Match Support:** Combine map results into a series overview with selectable per-map details.
- [ ] **Automated Data Pipeline:** Set up automated sync so match results automatically update `data/matches.json`.
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

`tools/faceit_sync.py` 不会在源代码中保存 API Key。运行脚本前，请在当前终端会话中设置
`FACEIT_API_KEY` 环境变量：

### Windows PowerShell

```powershell
$env:FACEIT_API_KEY = "你的新 FACEIT API Key"
python tools/faceit_sync.py
```

### Windows 命令提示符

```cmd
set FACEIT_API_KEY=你的新 FACEIT API Key
python tools/faceit_sync.py
```

如果旧 API Key 曾经提交到 Git 或公开仓库，请立即在 FACEIT 开发者后台撤销它并生成新 Key。
不要把新 Key 写入代码、`data/matches.json`、README 或提交到仓库。

### 同步 BO3

运行 `python -m tools.manage_matches` 添加比赛时，若有一个代表整场系列赛的 FACEIT 链接，选择“单个 FACEIT 链接”，粘贴该链接即可。若该链接的 FACEIT stats API 返回全部地图数据，脚本会自动识别系列赛比分，并保存每张图的比分和选手统计。

若 FACEIT 链接只对应一张地图，则使用 BO3 的“多个地图链接手动合并”方式，按比赛顺序输入 2 或 3 个地图对应的 Match 链接/ID。详情页提供系列赛总览和逐地图切换。旧记录若没有地图/选手数据，需要重新同步。

从项目根目录运行同步脚本即可；脚本会始终读写 `data/matches.json`，不受当前工作目录影响。

### 本地比赛管理

在项目根目录运行：

```powershell
python -m tools.manage_matches
```

管理菜单可列出本地比赛、拉取并添加 BO1/BO3 比赛，或按列表编号删除记录。拉取新比赛需要先设置 `FACEIT_API_KEY`；查看和删除不需要 API Key。变更会直接写入 `data/matches.json`，取消确认不会保存。完成后检查网站，再手动提交并 push 到 GitHub Pages。