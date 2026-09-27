document.addEventListener('DOMContentLoaded', () => {
    const matchListContainer = document.getElementById('match-list');

    fetch('matches.json')
        .then(response => response.json())
        .then(data => {
            data.forEach(match => {
                const card = document.createElement('div');
                card.className = 'card match-result';

                // 判断哪支队伍获胜，动态添加 winner 绿色高亮样式
                const teamAClass = match.winner === match.team_a ? 'team winner' : 'team';
                const teamBClass = match.winner === match.team_b ? 'team winner' : 'team';

                card.innerHTML = `
                    <div class="match-info">
                        <h3>${match.match_title}</h3>
                        <p>地图：${match.map}</p>
                    </div>
                    <div class="score-board">
                        <span class="${teamAClass}">${match.team_a}</span>
                        <span class="score">${match.score}</span>
                        <span class="${teamBClass}">${match.team_b}</span>
                    </div>
                `;

                matchListContainer.appendChild(card);
            });
        })
        .catch(error => console.error('加载比赛数据失败:', error));
});