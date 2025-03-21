# chatgpt_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import os

from .forms import SearchForm, ExportForm
from .models import SearchHistory
from .api_wrapper import ChatGPTAPI

# APIインスタンスをグローバルに作成
api_instance = ChatGPTAPI()

def index(request):
    """メインページ"""
    search_form = SearchForm()
    
    # セッションからAPIキーを復元
    if 'api_key' in request.session:
        search_form.fields['api_key'].initial = request.session['api_key']
    
    context = {
        'search_form': search_form,
        'page_title': '検索',
    }
    return render(request, 'chatgpt_app/index.html', context)

@require_http_methods(["POST"])
def search(request):
    """検索を実行"""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            api_key = form.cleaned_data['api_key']
            query = form.cleaned_data['query']
            
            # APIキーをセッションに保存
            request.session['api_key'] = api_key
            
            # APIキーを設定
            api_instance.set_api_key(api_key)
            
            # 検索を実行
            result = api_instance.search(query)
            
            if 'error' in result:
                return JsonResponse({'error': result['error']})
            
            # 検索結果をデータベースに保存
            history = SearchHistory(
                query=query,
                result=result['result'],
                model=result.get('model', 'gpt-4-turbo-preview'),
            )
            history.set_tokens(result.get('tokens', {}))
            history.save()
            
            return JsonResponse({
                'success': True,
                'result': result['result'],
                'tokens': result.get('tokens', {}),
                'timestamp': timezone.now().isoformat(),
                'history_id': history.id
            })
        
        return JsonResponse({'error': 'フォームが無効です。正しい値を入力してください。'})
    
    return JsonResponse({'error': '不正なリクエストメソッドです。'}, status=405)

def history(request):
    """履歴ページ"""
    histories = SearchHistory.objects.all()
    export_form = ExportForm()
    
    context = {
        'histories': histories,
        'export_form': export_form,
        'page_title': '履歴',
    }
    return render(request, 'chatgpt_app/history.html', context)

def history_detail(request, history_id):
    """履歴詳細をJSONで返す"""
    history = get_object_or_404(SearchHistory, id=history_id)
    return JsonResponse(history.to_dict())

@require_http_methods(["POST"])
def export_history(request):
    """履歴をJSONファイルとしてエクスポート"""
    if request.method == "POST":
        form = ExportForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data['filename']
            
            # ファイル名が指定されていない場合はデフォルト名を使用
            if not filename:
                filename = f"chatgpt_history_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # 拡張子がない場合は.jsonを追加
            if not filename.endswith('.json'):
                filename += '.json'
            
            # 履歴をJSONファイルに保存
            result = SearchHistory.export_to_json(filename)
            
            if 'error' in result:
                return JsonResponse({'error': result['error']})
            
            # ファイルをダウンロード
            with open(result['filename'], 'r', encoding='utf-8') as f:
                response = HttpResponse(f.read(), content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
            
            # 一時ファイルを削除
            os.remove(result['filename'])
            
            return response
        
        return JsonResponse({'error': 'フォームが無効です。正しい値を入力してください。'})
    
    return JsonResponse({'error': '不正なリクエストメソッドです。'}, status=405)

def delete_history(request, history_id):
    """履歴を削除"""
    if request.method == "POST":
        history = get_object_or_404(SearchHistory, id=history_id)
        history.delete()
        return redirect('history')
    
    return JsonResponse({'error': '不正なリクエストメソッドです。'}, status=405)