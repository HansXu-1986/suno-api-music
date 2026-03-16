#!/usr/bin/env python3
"""
Poll for generation result from MCP
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
    "task_ids": ["2033385400273211392", "2033385400273211393"]
}

messages_received = []
done_event = threading.Event()
music_urls = []

def handle_sse(client):
    """Handle incoming SSE events"""
    for event in client.events():
        print(f"[SSE] {event.event}: {event.data[:150]}...")
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
                            print(f"\n🎵 Got audio: {item.get('title')} -> {item.get('url')}")
                            music_urls.append({
                                "title": item.get('title', 'Untitled'),
                                "url": item.get('url'),
                                "duration": item.get('duration', 0)
                            })
                            if len(music_urls) == 2:
                                done_event.set()
                                return
            except Exception as e:
                print(f"Error parsing: {e}")
                pass
        # If we get any complete message, we're done
        if len(music_urls) > 0:
            done_event.set()

def main():
    headers = {
        "Authorization": f"Bearer {CONFIG['api_key']}",
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache"
    }
    
    print(f"Connecting to SSE...")
    
    try:
        response = requests.get(CONFIG['sse_url'], headers=headers, stream=True, timeout=120)
        response.raise_for_status()
        print(f"Connected! Status: {response.status_code}")
        
        client = sseclient.SSEClient(response)
        
        # Wait for endpoint
        endpoint_received = False
        post_url = None
        
        thread = threading.Thread(target=handle_sse, args=(client,))
        thread.daemon = True
        thread.start()
        
        # Wait for endpoint
        for _ in range(100):
            if messages_received and any(m['event'] == 'endpoint' for m in messages_received):
                endpoint_received = True
                endpoint_data = next(m['data'] for m in messages_received if m['event'] == 'endpoint')
                post_url = endpoint_data
                break
            time.sleep(0.1)
        
        if not endpoint_received:
            print("Timeout waiting for endpoint")
            return
        
        print(f"Message endpoint: {post_url}")
        
        post_headers = {
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "Content-Type": "application/json"
        }
        
        # Initialize
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {
                    "name": "suno-api-music",
                    "version": "1.0.0"
                },
                "capabilities": {}
            }
        }
        
        r = requests.post(post_url, json=init_request, headers=post_headers, timeout=30)
        print(f"Initialize: {r.status_code}")
        
        time.sleep(1)
        
        # Call get_generation_status
        check_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_generation_status",
                "arguments": {
                    "task_ids": CONFIG['task_ids']
                }
            }
        }
        
        print(f"\nQuerying status for tasks: {CONFIG['task_ids']}")
        r = requests.post(post_url, json=check_request, headers=post_headers, timeout=30)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 202:
            print("Accepted, waiting for completion (up to 90s)...")
            done_event.wait(timeout=90)
        elif r.status_code != 200:
            print(f"Response: {r.text}")
        
        # Wait a bit more for events to come through SSE
        time.sleep(5)
        
        print("\n" + "="*60)
        print("Final Result:")
        print("="*60)
        
        if music_urls:
            print(f"\n✅ Generation complete! {len(music_urls)} songs generated:")
            for i, music in enumerate(music_urls, 1):
                print(f"\n{i}. **{music['title']}**")
                print(f"   🔗 URL: {music['url']}")
                print(f"   ⏱️  Duration: {music['duration']} seconds")
        else:
            print("\n⏳ Still generating...")
            print("Task IDs are: " + ", ".join(CONFIG['task_ids']))
            print("Try again in 30 seconds with the same task IDs")
        
        # Print all messages for debugging
        print("\n" + "="*60)
        print("Debug - All messages:")
        print("="*60)
        for i, msg in enumerate(messages_received):
            print(f"[{i+1}] {msg['event']}: {msg['data'][:100]}...")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
