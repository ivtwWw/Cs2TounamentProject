document.addEventListener("DOMContentLoaded", () => {
    const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    }[character]));

    fetch('matches.json')
        .then(response => response.json())
        .then(data => {
            const matchListContainer = document.getElementById('match-list');
            if (!matchListContainer) return;

            let htmlContent = '';

            data.matches.forEach(match => {
                const teamAClass = match.winner === match.teamA ? 'winner' : '';
                const teamBClass = match.winner === match.teamB ? 'winner' : '';
                
                const matchDetail = match.info || match.map || match.details || '';

                const matchId = encodeURIComponent(match.id || '');
                const detailsUrl = matchId ? `match.html?id=${matchId}` : '';
                htmlContent += `
                    <a class="card match-result match-link" href="${detailsUrl}">
                        <div class="match-info">
                            <h3>${escapeHtml(match.stage)}</h3>
                            <p>${escapeHtml(matchDetail)}</p>
                        </div>
                        <div class="score-board">
                            <span class="score-team score-team-a ${teamAClass}">${escapeHtml(match.teamA)}</span>
                            <span class="score">${escapeHtml(match.score)}</span>
                            <span class="score-team score-team-b ${teamBClass}">${escapeHtml(match.teamB)}</span>
                        </div>
                        <span class="details-hint">${matchId ? '查看详情 →' : '暂无详情'}</span>
                    </a>
                `;
            });

            matchListContainer.innerHTML = htmlContent;
        })
        .catch(error => console.error('加载比赛数据失败:', error));
});