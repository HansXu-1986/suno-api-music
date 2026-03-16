#!/usr/bin/env python3
"""
Alipay Webhook Server for automatic Pro activation
Deploy this to your server and configure Alipay notify URL

Example deployment:
- Use Flask/Gunicorn to run
- Or deploy to Vercel as serverless function
- Or deploy to Render with free tier

Author: HansXu-1986
License: MIT
"""

import json
import os
from flask import Flask, request, jsonify
from alipay.aop.api.util.SignatureUtils import verify_sign
from alipay_auto_activate import AlipayAutoActivate

app = Flask(__name__)

# Load configuration from environment variables or config file
CONFIG = {
    "github_token": os.environ.get("GITHUB_TOKEN", ""),
    "gist_id": os.environ.get("GIST_ID", ""),
    "alipay_app_id": os.environ.get("ALIPAY_APP_ID", ""),
    "alipay_public_key": os.environ.get("ALIPAY_PUBLIC_KEY", ""),  # Alipay public key for signature verification
}

# Or load from config.json
if os.path.exists("webhook_config.json"):
    with open("webhook_config.json", "r") as f:
        config_data = json.load(f)
        CONFIG.update(config_data)


@app.route("/webhook/alipay", methods=["POST"])
def alipay_webhook():
    """Alipay asynchronous notification endpoint"""
    try:
        # Get POST data from Alipay
        post_data = request.form.to_dict()
        print(f"Received notification: {json.dumps(post_data, indent=2)}")
        
        # Verify signature
        sign = post_data.pop("sign", None)
        if not sign:
            print("No signature")
            return jsonify({"code": 400, "message": "No signature"}), 400
        
        # Verify the signature using Alipay public key
        # This is REQUIRED for security
        try:
            is_verified = verify_sign(
                post_data,
                sign,
                CONFIG["alipay_public_key"],
                "utf-8",
            )
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return jsonify({"code": 400, "message": "Signature verification failed"}), 400
        
        if not is_verified:
            print("Invalid signature")
            return jsonify({"code": 400, "message": "Invalid signature"}), 400
        
        # Check payment status
        trade_status = post_data.get("trade_status", "")
        if trade_status not in ["TRADE_SUCCESS", "TRADE_FINISHED"]:
            print(f"Payment not completed: {trade_status}")
            # Alipay will retry, so return success to stop retrying
            return jsonify({"code": 200, "message": f"Payment not completed: {trade_status}"}), 200
        
        # Get order number
        order_number = post_data.get("out_trade_no", "")
        if not order_number:
            print("No order number")
            return jsonify({"code": 400, "message": "No order number"}), 400
        
        # Check amount - should be 9.9 CNY
        total_amount = float(post_data.get("total_amount", 0))
        if total_amount < 9.9:
            print(f"Invalid amount: {total_amount}")
            return jsonify({"code": 400, "message": f"Invalid amount: {total_amount}"}), 400
        
        # Add activation code to Gist
        if not CONFIG["github_token"] or not CONFIG["gist_id"]:
            print("GitHub config missing")
            return jsonify({"code": 500, "message": "GitHub config missing"}), 500
        
        aa = AlipayAutoActivate(CONFIG["github_token"], CONFIG["gist_id"])
        success, msg = aa.add_activation_code(order_number)
        
        if success:
            print(f"✅ Successfully added activation code: {order_number}")
            return jsonify({
                "code": 200,
                "message": msg,
                "activation_code": order_number
            }), 200
        else:
            print(f"❌ Failed to add activation code: {msg}")
            return jsonify({"code": 500, "message": msg}), 500
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"code": 500, "message": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    """Health check"""
    return jsonify({
        "service": "suno-api-music alipay webhook",
        "status": "running",
        "gist_id": CONFIG["gist_id"]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
