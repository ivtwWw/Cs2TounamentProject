# CS2 Tournament Match Site 🎮

A clean, lightweight, and modern web application designed to track and display CS2 Aussie Laozi Cup tournament match results, powered by static hosting and dynamic JSON data rendering.

---

## 🚀 Current Features

- **Dynamic Data Rendering:** Match results and stats are decoupled into an external `matches.json` file and dynamically loaded via JavaScript, making data updates clean and modular.
- **Optimized Project Architecture:** Standardized flat frontend directory layout designed specifically for seamless GitHub Pages deployment without nested routing errors.
- **Zero-Dependency Frontend:** Built using pure HTML5, modern CSS, and Vanilla JavaScript for lightning-fast load times and easy maintenance.
- **Live Deployment:** Automatically deployed and publicly accessible via GitHub Pages.

---

## 📁 Project Structure

```text
cs2MatchSite/
├── 📄 index.html      # Main entry point of the website
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