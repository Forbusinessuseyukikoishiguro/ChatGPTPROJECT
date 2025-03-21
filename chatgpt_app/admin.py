from django.contrib import admin
from .models import SearchHistory

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    """検索履歴の管理画面設定"""
    list_display = ('id', 'short_query', 'timestamp', 'model', 'tokens_total')
    list_filter = ('model', 'timestamp')
    search_fields = ('query', 'result')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    def short_query(self, obj):
        """クエリの一部を表示"""
        return obj.query[:50] + '...' if len(obj.query) > 50 else obj.query
    
    short_query.short_description = '検索クエリ'