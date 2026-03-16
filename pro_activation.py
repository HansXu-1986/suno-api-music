#!/usr/bin/env python3
"""
Pro activation verification for suno-api-music
Automatically verify activation code from public GitHub Gist
"""

import json
import requests
from typing import Tuple


def verify_pro_activation(activation_code: str, activation_list_url: str) -> Tuple[bool, str]:
    """
    Verify if a Pro activation code is valid by checking the public Gist list
    
    Args:
        activation_code: The activation code from user config (usually Alipay order number)
        activation_list_url: Raw URL to the activated codes Gist
    
    Returns:
        (is_valid, message)
    """
    # If no activation code provided, it's base version
    if not activation_code or activation_code.strip() == "":
        return False, "No activation code provided - base version"
    
    # Trim whitespace
    activation_code = activation_code.strip()
    
    try:
        # Fetch the public activation list from Gist
        resp = requests.get(activation_list_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        activated_codes = data.get("activated_codes", [])
        
        if activation_code in activated_codes:
            return True, f"✅ Pro activation successful: {activation_code}"
        else:
            return False, f"❌ Activation code not found: {activation_code}\nPlease check your order number and try again."
    
    except Exception as e:
        return False, f"⚠️ Verification failed: {e}\nUsing base version (single generation only)."


def get_max_versions(default_versions: int, activation_code: str, activation_list_url: str) -> int:
    """
    Get the maximum allowed versions based on activation status
    
    - Base version: max 1 version
    - Pro version: max 10 versions
    """
    is_pro, _ = verify_pro_activation(activation_code, activation_list_url)
    if is_pro:
        # Pro version allows up to 10
        return min(default_versions, 10)
    else:
        # Base version only allows 1
        return 1
