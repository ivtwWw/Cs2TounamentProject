document.addEventListener("DOMContentLoaded", () => {
    const content = document.getElementById('about-content');
    const escapeHtml = (value) => value.replace(/[&<>"']/g, (character) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    }[character]));

    const renderInline = (text) => {
        let html = escapeHtml(text);
        html = html.replace(
            /\[([^\]]+)\]\((https?:\/\/[^\s)]+|mailto:[^\s)]+)\)/g,
            (_match, label, href) =>
                `<a href="${href}" target="_blank" rel="noopener noreferrer">${label}</a>`
        );
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
        return html;
    };

    const renderMarkdown = (markdown) => {
        const lines = markdown.replace(/\r\n/g, '\n').split('\n');
        const blocks = [];
        let paragraph = [];
        let listItems = [];

        const flushParagraph = () => {
            if (paragraph.length) {
                blocks.push(`<p>${paragraph.map(renderInline).join('<br>')}</p>`);
                paragraph = [];
            }
        };
        const flushList = () => {
            if (listItems.length) {
                blocks.push(`<ul>${listItems.map((item) => `<li>${renderInline(item)}</li>`).join('')}</ul>`);
                listItems = [];
            }
        };

        for (const line of lines) {
            const heading = line.match(/^(#{1,3})\s+(.+)$/);
            const listItem = line.match(/^\s*[-*]\s+(.+)$/);
            if (!line.trim()) {
                flushParagraph();
                flushList();
            } else if (heading) {
                flushParagraph();
                flushList();
                const level = heading[1].length;
                blocks.push(`<h${level}>${renderInline(heading[2])}</h${level}>`);
            } else if (listItem) {
                flushParagraph();
                listItems.push(listItem[1]);
            } else {
                flushList();
                paragraph.push(line.trim());
            }
        }

        flushParagraph();
        flushList();
        return blocks.join('\n');
    };

    fetch('docs/about.md')
        .then((response) => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.text();
        })
        .then((markdown) => {
            content.innerHTML = renderMarkdown(markdown);
        })
        .catch((error) => {
            console.error('加载关于我们文档失败:', error);
            content.innerHTML = '<p class="error-message">关于我们内容暂时无法加载。</p>';
        });
});
