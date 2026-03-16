#!/usr/bin/env python3
"""
Just ask "好了吗" to get the result
"""

import json
import requests
import sseclient
import threading
import time

# Configuration
CONFIG = {
    "sse_url": "https://mcp.suno.cn/mcp/sse",
    "api_key": "sk-4c213779d6d0749c513eba370885023eb0fb59bdad6156923fb540ddbbeb",
    "prompt": "好了吗"
}

messages_received = []
done_event = threading.Event()
music_urls = []

def handle_sse(client):
    for event in client.events():
        print(f"[SSE] {event.event}: {event.data[:200]}")
        messages_received.append({
            "event": event.event,
            "data": event.data
        })
        
        if event.event == "message":
            try:
                data = json.loads(event.data)
                if "result" in data and "content" in data.get("result", {}):
                    content = data["result"]["content"]
                    for item in content:
                        if item.get("type") == "audio":
                            music_urls.append({
                                "title": item.get('title', 'Untitled'),
                                "url": item.get('url'),
                                "duration": item.get('duration', 0)
                            })
                            print(f"\n🎵 Found audio: {item.get('title')} -> {item.get('url')}")
                            if len(music_urls) >= 2:
                                done_event.set()
                                return
            except Exception as e:
                print(f"Parse error: {e}")
                pass
            
            # If we have any content, we are done
            if music_urls:
                done_event.set()

def main():
    headers = {
        "Authorization": f"Bearer {CONFIG['api_key']}",
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache"
    }
    
    print(f"Connecting to {CONFIG['sse_url']}...")
    response = requests.get(CONFIG['sse_url'], headers=headers, stream=True, timeout=60)
    response.raise_for_status()
    print(f"Connected: {response.status_code}")
    
    client = sseclient.SSEClient(response)
    
    thread = threading.Thread(target=handle_sse, args=(client,))
    thread.daemon = True
    thread.start()
    
    # Wait for endpoint
    post_url = None
    for _ in range(100):
        if messages_received and any(m['event'] == 'endpoint' for m in messages_received):
            post_url = next(m['data'] for m in messages_received if m['event'] == 'endpoint')
            break
        time.sleep(0.1)
    
    if not post_url:
        print("No endpoint received")
        return
    
    print(f"Post URL: {post_url}")
    
    post_headers = {
        "Authorization": f"Bearer {CONFIG['api_key']}",
        "Content-Type": "application/json"
    }
    
    # Initialize
    init = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "clientInfo": {"name": "test", "version": "1.0"},
            "capabilities": {}
        }
    }
    r = requests.post(post_url, json=init, headers=post_headers, timeout=30)
    print(f"Initialize: {r.status_code}")
    
    time.sleep(1)
    
    # Just send a text message "好了吗"
    # Actually it's a tool call to chat
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "chat",
            "arguments": {
                "message": "好了吗"
            }
        }
    }
    
    print(f"\nSending: 好了吗")
    r = requests.post(post_url, json=request, headers=post_headers, timeout=30)
    print(f"Response: {r.status_code}")
    
    # Wait for result
    print("\nWaiting for result... (60s timeout)")
    done_event.wait(timeout=60)
    
    time.sleep(3)
    
    print("\n" + "="*70)
    print("RESULT:")
    print("="*70)
    
    if music_urls:
        print(f"\n✅ 成功生成 {len(music_urls)} 首音乐！")
        for i, music in enumerate(music_urls, 1):
            print(f"\n{i}. {music['title']}")
            print(f"   🔗 {music['url']}")
            print(f"   ⏱️  {music['duration']}s")
    else:
        print("\n⏳ 还在生成中，再过一会试试")
        for msg in messages_received:
            if msg['event'] == 'message':
                print(f"Message: {msg['data']}")

if __name__ == "__main__":
    main()
