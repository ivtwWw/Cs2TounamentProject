document.addEventListener("DOMContentLoaded", () => {
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

                htmlContent += `
                    <div class="card match-result">
                        <div class="match-info">
                            <h3>${match.stage}</h3>
                            <p>${matchDetail}</p>
                        </div>
                        <div class="score-board">
                            <span class="${teamAClass}">${match.teamA}</span>
                            <span class="score">${match.score}</span>
                            <span class="${teamBClass}">${match.teamB}</span>
                        </div>
                    </div>
                `;
            });

            matchListContainer.innerHTML = htmlContent;
        })
        .catch(error => console.error('加载比赛数据失败:', error));
});