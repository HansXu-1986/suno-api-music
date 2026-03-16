#!/usr/bin/env python3
"""
Test script for suno.cn MCP API music generation
"""

import json
import requests
import sseclient
import time

# Configuration
CONFIG = {
    "sse_url": "https://mcp.suno.cn/mcp/sse",
    "api_key": "sk-4c213779d6d0749c513eba370885023eb0fb59bdad6156923fb540ddbbeb",
    "prompt": "中国风RAP，批判当今社会人情淡薄、金钱至上，同时包含祝愿发财的内容，呈现矛盾复杂的情感",
    "make_instrumental": False,
    "wait_audio": True
}

def main():
    headers = {
        "Authorization": f"Bearer {CONFIG['api_key']}",
        "Accept": "text/event-stream"
    }
    
    print(f"Connecting to {CONFIG['sse_url']}...")
    
    try:
        response = requests.get(CONFIG['sse_url'], headers=headers, stream=True, timeout=120)
        response.raise_for_status()
        
        client = sseclient.SSEClient(response)
        
        print("Connected! Waiting for endpoint...")
        
        endpoint = None
        for event in client.events():
            if event.event == 'endpoint':
                endpoint = event.data
                print(f"Got endpoint: {endpoint}")
                break
            elif event.event:
                print(f"Event {event.event}: {event.data}")
        
        if not endpoint:
            print("No endpoint received from SSE")
            return
        
        # Now send the generate request via POST
        # endpoint can be full URL or just path
        if endpoint.startswith('http'):
            post_url = endpoint
        elif endpoint.startswith('/'):
            post_url = f"https://mcp.suno.cn{endpoint}"
        else:
            post_url = f"https://mcp.suno.cn/{endpoint}"
        print(f"Sending generate request to {post_url}")
        
        # MCP initialize request
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
        
        post_headers = {
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "Content-Type": "application/json"
        }
        
        r = requests.post(post_url, json=init_request, headers=post_headers, timeout=30)
        print(f"Initialize response: {r.status_code}")
        if r.status_code != 200:
            print(r.text)
            return
        
        print("Initialize done")
        
        # Send music generate request
        # The tool name should be 'generate_music'
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
        
        r = requests.post(post_url, json=generate_request, headers=post_headers, timeout=60)
        print(f"Generate request response: {r.status_code}")
        if r.status_code == 200:
            result = r.json()
            print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(r.text)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
