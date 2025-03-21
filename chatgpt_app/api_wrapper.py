# chatgpt_app/api_wrapper.py

import requests
import json
from datetime import datetime
import os

class ChatGPTAPI:
    """
    ChatGPT APIとのやり取りを管理するクラス
    """
    def __init__(self, api_key=None):
        """初期化"""
        self.api_key = api_key
        self.history = []
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
    def set_api_key(self, api_key):
        """APIキーを設定"""
        self.api_key = api_key
    
    def search(self, query, model="gpt-4-turbo-preview", max_tokens=2000, temperature=0.7):
        """
        検索を実行
        
        Args:
            query (str): 検索クエリ
            model (str): 使用するモデル
            max_tokens (int): 最大トークン数
            temperature (float): 温度（創造性の度合い）
            
        Returns:
            dict: 検索結果、エラーがあればエラー情報
        """
        if not self.api_key:
            return {"error": "APIキーが設定されていません"}
        
        if not query.strip():
            return {"error": "検索クエリが空です"}
        
        try:
            # OpenAI APIにリクエスト
            response = requests.post(
                self.base_url,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_key}'
                },
                json={
                    'model': model,
                    'messages': [
                        {'role': 'system', 'content': 'あなたは役立つアシスタントです。ユーザーの質問に答えてください。'},
                        {'role': 'user', 'content': query}
                    ],
                    'max_tokens': max_tokens,
                    'temperature': temperature
                },
                timeout=60  # タイムアウト設定
            )
            
            # レスポンスの確認
            if response.status_code != 200:
                return {
                    "error": f"APIリクエストが失敗しました (ステータスコード: {response.status_code})",
                    "details": response.text
                }
            
            data = response.json()
            
            if 'error' in data:
                return {"error": data['error']['message']}
            
            # 結果を取得
            result = data['choices'][0]['message']['content']
            tokens = data.get('usage', {})
            timestamp = datetime.now().isoformat()
            
            # 履歴に追加
            history_item = {
                'id': len(self.history) + 1,
                'query': query,
                'result': result,
                'tokens': tokens,
                'timestamp': timestamp,
                'model': model
            }
            self.history.append(history_item)
            
            return {
                "success": True,
                "result": result,
                "tokens": tokens,
                "timestamp": timestamp,
                "history_id": history_item['id']
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"リクエスト中にエラーが発生しました: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "APIからのレスポンスをJSONとして解析できませんでした"}
        except Exception as e:
            return {"error": f"予期しないエラーが発生しました: {str(e)}"}
    
    def get_history(self):
        """検索履歴を取得"""
        return self.history
    
    def get_history_item(self, history_id):
        """特定の履歴アイテムを取得"""
        for item in self.history:
            if item['id'] == history_id:
                return item
        return None
    
    def save_history_to_file(self, filename=None):
        """検索履歴をJSONファイルに保存"""
        if not filename:
            filename = f"chatgpt_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return {"success": True, "filename": filename}
        except Exception as e:
            return {"error": f"ファイル保存中にエラーが発生しました: {str(e)}"}