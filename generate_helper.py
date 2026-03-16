#!/usr/bin/env python3
"""
Generation helper for suno-api-music
Supports:
- Auto mode: one sentence → generate
- Custom mode: step-by-step inquiry → confirm → generate
"""

from typing import Dict, Optional, Tuple


def parse_auto_mode(user_input: str) -> Dict:
    """Parse user input from auto mode - one sentence generation"""
    return {
        "prompt": user_input.strip(),
        "lyrics": None,
        "title": None,
        "style": None,
        "instrumental": False,
        "versions": None,
    }


def start_custom_mode() -> str:
    """Start custom mode - return first question"""
    return """🎵 自定义生成模式 - 请回答以下问题：

1️⃣ 请描述你想要的歌曲主题/歌词大意："""


def get_next_question(current_step: int, answers: Dict) -> Optional[str]:
    """Get next question based on current step"""
    steps = [
        ("prompt", "1️⃣ 请描述你想要的歌曲主题/歌词大意："),
        ("style", "2️⃣ 请指定歌曲风格/曲风（例如：中国风RAP、流行民谣、摇滚、爵士）："),
        ("title", "3️⃣ 请指定歌曲标题（留空自动生成）："),
        ("lyrics", "4️⃣ 如果需要指定完整歌词，请粘贴在这里（留空让 AI 创作）："),
        ("instrumental", "5️⃣ 需要纯音乐吗？（是/否，默认否）："),
        ("versions", "6️⃣ 需要生成几个版本？（1-10，默认 2）："),
    ]
    
    if current_step < len(steps):
        return steps[current_step][1]
    return None


def process_answer(current_step: int, answer: str, answers: Dict) -> Dict:
    """Process user answer and return updated answers"""
    steps = ["prompt", "style", "title", "lyrics", "instrumental", "versions"]
    key = steps[current_step]
    
    answer = answer.strip()
    
    if key == "instrumental":
        answers[key] = answer.lower() in ["是", "yes", "y", "true", "对"]
    elif key == "versions":
        try:
            answers[key] = int(answer)
        except:
            answers[key] = 2
    else:
        answers[key] = answer if answer else None
    
    return answers


def is_custom_mode_complete(answers: Dict) -> bool:
    """Check if all required questions are answered"""
    required = ["prompt"]
    for req in required:
        if req not in answers or answers[req] is None:
            return False
    return True


def summarize_custom_request(answers: Dict) -> str:
    """Generate summary for user confirmation"""
    summary = ["📋 生成信息确认：\n"]
    
    if answers.get("prompt"):
        summary.append(f"**主题/歌词大意**: {answers['prompt']}")
    
    if answers.get("style"):
        summary.append(f"**曲风**: {answers['style']}")
    
    if answers.get("title"):
        summary.append(f"**标题**: {answers['title']}")
    
    if answers.get("lyrics"):
        summary.append(f"**指定歌词**: {answers['lyrics'][:100]}{'...' if len(answers['lyrics']) > 100 else ''}")
    
    if answers.get("instrumental"):
        summary.append("**纯音乐**: 是")
    else:
        summary.append("**纯音乐**: 否")
    
    versions = answers.get("versions", 2)
    summary.append(f"**生成版本数**: {versions}")
    
    summary.append("\n✓ 确认以上信息无误，请回复「确认」开始生成")
    summary.append("✓ 如果需要修改，请回复需要修改的内容")
    
    return "\n".join(summary)


def build_generation_request(answers: Dict) -> Dict:
    """Build final generation request for MCP API"""
    prompt = answers.get("prompt", "")
    
    # Combine all info into one prompt
    full_prompt = prompt
    
    if answers.get("style"):
        full_prompt += f"\n风格: {answers['style']}"
    
    if answers.get("title"):
        full_prompt += f"\n标题: {answers['title']}"
    
    if answers.get("lyrics"):
        full_prompt += f"\n歌词: {answers['lyrics']}"
    
    return {
        "prompt": full_prompt,
        "title": answers.get("title"),
        "style": answers.get("style"),
        "lyrics": answers.get("lyrics"),
        "make_instrumental": answers.get("instrumental", False),
        "versions": answers.get("versions", 2),
    }


def handle_mode_selection(user_input: str) -> Tuple[str, Optional[Dict]]:
    """
    Handle user initial request, detect if it's auto or custom mode
    Returns: (mode, None) where mode is "auto" or "custom"
    """
    user_input_lower = user_input.lower()
    
    # User explicitly requested custom
    if any(word in user_input_lower for word in ["自定义", "custom", "分步", "询问"]):
        return "custom", None
    
    # User explicitly requested auto
    if any(word in user_input_lower for word in ["自动", "auto", "一句话"]):
        return "auto", parse_auto_mode(user_input)
    
    # Default: if user just described the song, use auto mode
    return "auto", parse_auto_mode(user_input)
