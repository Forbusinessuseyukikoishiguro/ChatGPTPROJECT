// 共通のユーティリティ関数

// APIキーをセッションストレージに保存
function saveApiKeyToStorage(apiKey) {
    if (apiKey) {
        sessionStorage.setItem('api_key', apiKey);
    }
}

// APIキーをセッションストレージから復元
function loadApiKeyFromStorage() {
    const apiKeyInput = document.getElementById('id_api_key');
    if (apiKeyInput) {
        const savedApiKey = sessionStorage.getItem('api_key');
        if (savedApiKey) {
            apiKeyInput.value = savedApiKey;
        }
    }
}

// 日時フォーマット
function formatTime(date) {
    if (!date) return '';
    
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    return date.toLocaleString('ja-JP', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// テキストを指定の長さで切り詰める
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// ページ読み込み時の共通処理
document.addEventListener('DOMContentLoaded', function() {
    // APIキーをセッションストレージから復元
    loadApiKeyFromStorage();
});