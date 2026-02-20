import secrets
import string
import requests
from django.conf import settings
from googleapiclient.discovery import build
from rest_framework.response import Response

def ApiResponse(data=None, message="Success", status="success", status_code=200, **kwargs):
    # Handle common mistake where status is used instead of status_code
    if isinstance(status, int):
        status_code = status
        status = 'error'
    
    # Automatically set status to 'error' for failure codes if still at default
    if status_code >= 400 and status == 'success':
        status = 'error'

    response_data = {
        "status": status,
        "message": message,
    }
    
    if data is not None:
        response_data['data'] = data
        
    if kwargs:
        response_data.update(kwargs)
        
    return Response(response_data, status=status_code)

def generate_password(length=12):
    # ... (existing code)
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            return password

def get_meta(url, type='', api_key=None):
    """
    Port of Laravel helper get_meta.
    Fetches social media metadata (YouTube followers/channel info).
    """
    result = {
        'name': None,
        'description': None,
        'icon': None,
        'views': 0,
        'likes': 0,
        'followers': 0,
        'comments': 0,
        'topic_details': None
    }
    
    if 'youtube.com' in url or 'youtu.be' in url:
        yt_api_key = api_key or getattr(settings, 'GOOGLE_API_KEY', None)
        if not yt_api_key:
            return result
        
        try:
            youtube = build('youtube', 'v3', developerKey=yt_api_key)
            
            # Simple channel info fetch if type is link/followers
            if type == 'followers' or type == 'link':
                # Need to extract channel ID or use forHandle/forUsername if in URL
                # Simplified: assuming URL contains channel ID or handle
                parts = url.split('/')
                channel_id = None
                handle = None
                
                if '/channel/' in url:
                    channel_id = url.split('/channel/')[1].split('?')[0]
                elif '/@' in url:
                    handle = url.split('/@')[1].split('?')[0]
                
                if channel_id:
                    request = youtube.channels().list(part="snippet,statistics,topicDetails", id=channel_id)
                elif handle:
                    request = youtube.channels().list(part="snippet,statistics,topicDetails", forHandle=handle)
                else:
                    return result # Could not parse
                
                response = request.execute()
                if response.get('items'):
                    item = response['items'][0]
                    stats = item.get('statistics', {})
                    snippet = item.get('snippet', {})
                    result['name'] = snippet.get('title')
                    result['description'] = snippet.get('description')
                    result['followers'] = int(stats.get('subscriberCount', 0))
                    result['views'] = int(stats.get('viewCount', 0))
                    result['topic_details'] = item.get('topicDetails')
                    
        except Exception:
            pass # Or log error
            
    return result

def send_slack_notification(webhook_key, content):
    """
    Sends a notification to a Slack webhook.
    """
    # Assuming Setting model is available or fetched
    from .models import Setting
    try:
        webhook_url = Setting.objects.get(key=webhook_key).value
        if webhook_url:
            requests.post(webhook_url, json={"text": content})
    except Exception:
        pass
