function addRow() {
    const div = document.createElement('div');
    div.className = 'item-row';
    div.innerHTML = `
        <input type="text" name="subs[]" placeholder="Subreddit" required>
        <input type="text" name="kws[]" placeholder="Keywords" required>
        <button type="button" style="background:#e74c3c; color:white; border:none; border-radius:6px; padding:0 15px; cursor:pointer;" onclick="this.parentElement.remove()">-</button>
    `;
    document.getElementById('fields').appendChild(div);
}

// Привязываем событие при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('mainForm');
    if (form) {
        form.onsubmit = function() {
            const s = document.getElementsByName('subs[]');
            const k = document.getElementsByName('kws[]');
            const l = document.querySelector('input[name="limit"]').value;
            const items = [];

            for(let i=0; i<s.length; i++) {
                items.push({
                    "subreddit": s[i].value,
                    "keywords": k[i].value.split(',').map(x => x.trim())
                });
            }

            document.getElementById('hidden_json').value = JSON.stringify({
                "items": items,
                "limit": parseInt(l)
            });
        };
    }
});
