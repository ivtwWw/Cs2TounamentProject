document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('match-detail');
    const matchId = new URLSearchParams(window.location.search).get('id');

    const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    }[character]));

    const stat = (player, key) => player.stats?.[key] ?? player[key] ?? '-';

    if (!matchId) {
        container.innerHTML = '<p class="error-message">缺少比赛 ID。</p>';
        return;
    }

    fetch('matches.json')
        .then((response) => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then((data) => {
            const match = data.matches.find((item) => item.id === matchId);
            if (!match) {
                container.innerHTML = '<p class="error-message">找不到这场比赛。</p>';
                return;
            }

            const teams = match.details?.teams || [];
            const players = teams.flatMap((team) => team.players || []);
            const teamClass = (team) => team.name === match.winner ? 'winner' : '';
            const teamMarkup = teams.length
                ? teams.map((team) => `
                    <section class="team-detail card">
                        <h3 class="${teamClass(team)}">${escapeHtml(team.name)}</h3>
                        <div class="table-wrapper">
                            <table>
                                <thead><tr>
                                    <th>选手</th><th>K</th><th>D</th><th>A</th>
                                    <th>K/D</th><th>爆头率</th><th>ADR</th><th>得分</th>
                                </tr></thead>
                                <tbody>${(team.players || []).map((player) => `
                                    <tr>
                                        <td>${escapeHtml(player.nickname)}</td>
                                        <td>${escapeHtml(stat(player, 'Kills'))}</td>
                                        <td>${escapeHtml(stat(player, 'Deaths'))}</td>
                                        <td>${escapeHtml(stat(player, 'Assists'))}</td>
                                        <td>${escapeHtml(stat(player, 'K/D Ratio'))}</td>
                                        <td>${escapeHtml(stat(player, 'Headshots %'))}</td>
                                        <td>${escapeHtml(stat(player, 'ADR'))}</td>
                                        <td>${escapeHtml(stat(player, 'Score'))}</td>
                                    </tr>
                                `).join('')}</tbody>
                            </table>
                        </div>
                    </section>
                `).join('')
                : '<div class="card empty-state">这场比赛暂时没有选手个人数据。旧比赛需要重新同步后才会包含详细统计。</div>';

            container.innerHTML = `
                <a class="back-link" href="index.html#history">← 返回历史战绩</a>
                <section class="card match-summary">
                    <p class="match-stage">${escapeHtml(match.stage)}</p>
                    <h2>${escapeHtml(match.teamA)} <span> ${escapeHtml(match.score)} </span> ${escapeHtml(match.teamB)}</h2>
                    <p>${escapeHtml(match.info || match.map || '')}</p>
                    ${match.faceitUrl ? `<a class="btn" href="${escapeHtml(match.faceitUrl)}" target="_blank" rel="noopener">在 FACEIT 查看</a>` : ''}
                </section>
                ${teamMarkup}
                ${players.length === 0 && teams.length ? '<p class="empty-state">暂无选手统计数据。</p>' : ''}
            `;
        })
        .catch((error) => {
            console.error('加载比赛详情失败:', error);
            container.innerHTML = '<p class="error-message">加载比赛详情失败，请稍后重试。</p>';
        });
});
