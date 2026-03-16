#!/usr/bin/env python3
"""
Test script for suno.cn MCP API music generation - corrected MCP protocol
"""

import json
import requests
import sseclient
from urllib.parse import urljoin

# Configuration
CONFIG = {
    "base_url": "https://mcp.suno.cn",
    "sse_path": "/mcp/sse",
    "api_key": "sk-4c213779d6d0749c513eba370885023eb0fb59bdad6156923fb540ddbbeb",
    "prompt": "中国风RAP，批判当今社会人情淡薄、金钱至上，同时包含祝愿发财的内容，呈现矛盾复杂的情感",
    "make_instrumental": False,
    "wait_audio": True
}

def main():
    headers = {
        "Authorization": f"Bearer {CONFIG['api_key']}",
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache"
    }
    
    sse_url = urljoin(CONFIG['base_url'], CONFIG['sse_path'])
    print(f"Connecting to SSE: {sse_url}...")
    
    try:
        response = requests.get(sse_url, headers=headers, stream=True, timeout=120)
        response.raise_for_status()
        print(f"Connected, status: {response.status_code}")
        
        client = sseclient.SSEClient(response)
        
        # Get the endpoint URL for POST messages
        message_post_url = None
        session_id = None
        
        for event in client.events():
            print(f"Received event: {event.event} -> {event.data}")
            
            if event.event == 'endpoint':
                # The endpoint event gives us the URL to send messages to
                endpoint_path = event.data
                message_post_url = urljoin(CONFIG['base_url'], endpoint_path)
                print(f"Message endpoint: {message_post_url}")
                
                # Extract session ID from URL if needed
                if 'sessionId=' in endpoint_path:
                    session_id = endpoint_path.split('sessionId=')[1].split('&')[0]
                    print(f"Session ID: {session_id}")
                break
        
        if not message_post_url:
            print("No message endpoint received")
            return
        
        # Now send initialize
        post_headers = {
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "Content-Type": "application/json"
        }
        
        # Initialize
        init_msg = {
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
        
        print(f"\nSending initialize...")
        r = requests.post(message_post_url, json=init_msg, headers=post_headers, timeout=30)
        print(f"Initialize: {r.status_code}")
        if r.status_code != 200:
            print(f"Response: {r.text}")
            return
        
        init_result = r.json()
        print(f"Server info: {init_result.get('result', {}).get('serverInfo', {})}")
        
        # Now send the tools call
        print(f"\nSending generate_music request...")
        print(f"Prompt: {CONFIG['prompt']}")
        
        generate_msg = {
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
        
        r = requests.post(message_post_url, json=generate_msg, headers=post_headers, timeout=120)
        print(f"Generate: {r.status_code}")
        
        if r.status_code == 200:
            result = r.json()
            print(f"\nResult:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # Check if we have content
            if 'result' in result:
                content = result['result'].get('content', [])
                if content:
                    print("\n🎵 Generated music:")
                    for item in content:
                        if item.get('type') == 'audio':
                            print(f"  - {item.get('title', 'Untitled')}: {item.get('url', 'No URL')}")
        else:
            print(f"Error response: {r.text}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
