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
├── 📄 series.html                # One edition's match list
├── 📄 match.html                 # Match detail page
├── 📄 about.html                 # About the community tournament
├── 📄 _config.yml                # Keep Markdown files available as raw content
├── 📁 assets/
│   ├── 📁 css/
│   │   └── 📄 style.css          # Site styles
│   └── 📁 js/
│       ├── 📄 script.js          # Match list rendering
│       ├── 📄 series.js           # Edition match list rendering
│       ├── 📄 match.js           # Match detail rendering
│       └── 📄 about.js           # Markdown content rendering
├── 📁 data/
│   └── 📄 matches.json           # Editions, match results, and player statistics
├── 📁 tools/
│   ├── 📄 faceit_sync.py         # FACEIT match data sync helpers
│   └── 📄 manage_matches.py      # Local match management menu
├── 📁 docs/
│   ├── 📄 about.md               # Editable About Us content
│   └── 📄 changelog.md           # Change history
└── 📄 README.md                  # Project documentation
```

首页以赛事届次为单位展示 S1、S2 等系列赛；点进届次后查看该届比赛，单场详情仍可查看地图和选手数据。赛事数据按 `data/matches.json` 的 `series[]` 分组，每个系列赛包含 `id`、`title`、`status`、`description` 和 `matches[]`，并可选填 `eventTime`（比赛时间）及 `schedule`（赛程信息）；这两项显示在主页系列赛卡片和对应届次详情中。
已结束的届次还可记录 `championTeam`、`captain`、`mvp` 和 `championPlayers`。冠军队员的 FACEIT ID 和头像信息会展示在系列赛详情中；赛事 MVP 的 K/D、ADR、爆头率、击杀、死亡、助攻和单场 MVP 数根据本届地图统计汇总。Rating 需要手动填写，不会由网站推算。

“关于我们”页面的文案位于 `docs/about.md`。直接编辑该 Markdown 文件即可更新页面正文，支持标题、段落、无序列表、粗体、斜体和链接；无需修改 HTML 或 JavaScript。

---

## 🔮 Roadmap / Next Development Steps

- [x] **FACEIT API Integration:** Fetch match and player stats from the FACEIT API using `tools/faceit_sync.py`.
- [x] **BO3 Match Support:** Combine map results into a series overview with selectable per-map details.
- [x] **Series Management:** Organize seasons such as S1 and S2, with each season containing its own matches.
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

管理菜单可列出系列赛和比赛、拉取并添加 BO1/BO3 比赛、按列表编号删除记录、创建新系列赛、更新系列赛状态/比赛时间/赛程信息，以及编辑冠军队、队长、MVP、赛事 Rating 和冠军队员头像。更新系列赛信息时，时间可填写为自由格式（如 `2026年9月1日—9月15日`）；多条赛程阶段可用分号分隔，留空保持原值，输入 `-` 清除。拉取新比赛需要先设置 `FACEIT_API_KEY`；查看和删除不需要 API Key。变更会直接写入 `data/matches.json`，取消确认不会保存。完成后检查网站，再手动提交并 push 到 GitHub Pages。

要录入或修改主页显示的赛事时间和赛程：运行管理菜单，选择 `5. 更新系列赛信息（状态、比赛时间、赛程）`，再选对应届次。时间支持自由文本；赛程节点用分号分隔后会逐行显示在主页历届赛事卡片和届次详情页。字段留空会保留原内容，输入 `-` 可清除时间或赛程。

赛事结束后运行 `python -m tools.manage_matches`，选择菜单 `6` 登记冠军、队长和 MVP。MVP 的赛事总 Rating 需要手动输入；其他统计根据本届已同步的地图数据自动汇总。冠军队成员和 FACEIT ID 从总决赛数据读取，管理菜单会逐一提供头像 URL 补录项。主页历届赛事卡片展示冠军、队长和 MVP；点入届次后可查看冠军队阵容及 MVP 完整统计。

要创建 S2 或后续届次，在管理菜单选择“创建系列赛”，填写 ID（如 `s2`）、标题、简介和状态。添加比赛时选择它所属的系列赛；S1、S2 的比赛不会再混在同一个列表里。