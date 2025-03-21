# chatgpt_app/models.py

from django.db import models
from django.utils import timezone
import json

class SearchHistory(models.Model):
    """検索履歴モデル"""
    query = models.TextField(verbose_name="検索クエリ")
    result = models.TextField(verbose_name="検索結果")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="検索日時")
    model = models.CharField(max_length=50, verbose_name="使用モデル")
    tokens_prompt = models.IntegerField(null=True, blank=True, verbose_name="プロンプトトークン")
    tokens_completion = models.IntegerField(null=True, blank=True, verbose_name="完了トークン")
    tokens_total = models.IntegerField(null=True, blank=True, verbose_name="合計トークン")
    
    class Meta:
        verbose_name = "検索履歴"
        verbose_name_plural = "検索履歴"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.query[:30]}..."
    
    def set_tokens(self, tokens_dict):
        """トークン使用量を設定"""
        if tokens_dict:
            self.tokens_prompt = tokens_dict.get('prompt_tokens')
            self.tokens_completion = tokens_dict.get('completion_tokens')
            self.tokens_total = tokens_dict.get('total_tokens')
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'query': self.query,
            'result': self.result,
            'timestamp': self.timestamp.isoformat(),
            'model': self.model,
            'tokens': {
                'prompt_tokens': self.tokens_prompt,
                'completion_tokens': self.tokens_completion,
                'total_tokens': self.tokens_total
            }
        }
    
    @classmethod
    def export_to_json(cls, filename=None):
        """全履歴をJSONファイルに保存"""
        if not filename:
            filename = f"chatgpt_history_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            histories = cls.objects.all()
            data = [history.to_dict() for history in histories]
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return {"success": True, "filename": filename}
        except Exception as e:
            return {"error": f"ファイル保存中にエラーが発生しました: {str(e)}"}