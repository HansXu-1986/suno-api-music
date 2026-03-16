#!/usr/bin/env python3
"""
Test script for suno.cn MCP API - Correct SSE flow according to MCP spec
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
    "prompt": "中国风RAP，批判当今社会人情淡薄、金钱至上，同时包含祝愿发财的内容，呈现矛盾复杂的情感",
    "make_instrumental": False,
    "wait_audio": True
}

messages_received = []
done_event = threading.Event()

def handle_sse(client):
    """Handle incoming SSE events"""
    for event in client.events():
        print(f"\n[SSE] Event: {event.event} -> {event.data[:200]}...")
        messages_received.append({
            "event": event.event,
            "data": event.data
        })
        
        if event.event == "endpoint":
            print(f"[SSE] Got endpoint: {event.data}")
        
        # Check if we got the music result
        if event.event == "message" and "\"result\"" in event.data and "content" in event.data:
            print("[SSE] Got generation result!")
            done_event.set()
            break
        
        if event.event == "message" and "\"error\"" in event.data:
            print("[SSE] Got error!")
            done_event.set()
            break

def main():
    headers = {
        "Authorization": f"Bearer {CONFIG['api_key']}",
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache"
    }
    
    print(f"Connecting to SSE: {CONFIG['sse_url']}...")
    
    try:
        response = requests.get(CONFIG['sse_url'], headers=headers, stream=True, timeout=120)
        response.raise_for_status()
        print(f"Connected! Status: {response.status_code}")
        
        client = sseclient.SSEClient(response)
        
        # Start SSE listening thread
        thread = threading.Thread(target=handle_sse, args=(client,))
        thread.daemon = True
        thread.start()
        
        # Wait for endpoint event
        endpoint_received = False
        post_url = None
        
        # Wait up to 10 seconds for endpoint
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
        
        print(f"Got message endpoint: {post_url}")
        
        # Now send initialize via POST
        post_headers = {
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "Content-Type": "application/json"
        }
        
        # Initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {
                    "name": "suno-api-music-test",
                    "version": "1.0.0"
                },
                "capabilities": {}
            }
        }
        
        print(f"\nSending initialize request to {post_url}")
        r = requests.post(post_url, json=init_request, headers=post_headers, timeout=30)
        print(f"Initialize POST status: {r.status_code}")
        if r.status_code != 200:
            print(f"Response: {r.text}")
        
        # Wait for initialize response via SSE
        time.sleep(2)
        
        # Now send generate_music
        generate_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "generate_music",
                "arguments": {
                    "prompt": CONFIG['prompt'],
                    "make_instrumental": CONFIG['make_instrumental'],
                    "wait_audio": CONFIG['wait_audio']
                }
            }
        }
        
        print(f"\nSending generate_music request...")
        print(f"Prompt: {CONFIG['prompt']}")
        r = requests.post(post_url, json=generate_request, headers=post_headers, timeout=30)
        print(f"Generate POST status: {r.status_code}")
        if r.status_code != 200:
            print(f"Response: {r.text}")
        
        # Wait for result via SSE
        print("\nWaiting for generation completion (timeout 120s)...")
        done_event.wait(timeout=120)
        
        # Print all received messages
        print("\n" + "="*60)
        print("All messages received via SSE:")
        print("="*60)
        for i, msg in enumerate(messages_received):
            print(f"\n[{i+1}] event: {msg['event']}")
            try:
                parsed = json.loads(msg['data'])
                print(f"    data: {json.dumps(parsed, indent=2, ensure_ascii=False)}")
            except:
                print(f"    data (raw): {msg['data']}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
