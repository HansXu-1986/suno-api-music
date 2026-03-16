#!/usr/bin/env python3
"""
Advanced lyric generator for suno-api-music
Generates detailed tagged lyrics with per-line emotion, vocal, pace tags according to suno.cn specification
"""

from typing import List, Dict

def generate_detailed_lyric(
    theme: str,
    genre: str,
    title: str,
    style: str,
    instrumental: bool,
    instruments: str = None,
) -> str:
    """
    Generate detailed tagged lyrics with per-line processing
    
    Args:
        theme: Overall theme
        genre: Music genre
        title: Song title
        style: Overall style
        instrumental: Is instrumental?
        instruments: Instruments description
    """
    # Add global metadata tags
    lines = []
    lines.append(f"[title: {title}]")
    lines.append(f"[genre: {genre}]")
    if instruments:
        lines.append(f"[instrument: {instruments}]")
    lines.append(f"[style: {style}]")
    lines.append("")
    
    return "\n".join(lines)


def add_verse(
    lines: List[str],
    verse_lines: List[str],
    overall_emotion: str = "neutral",
) -> None:
    """Add a verse with per-line tagging"""
    lines.append(f"[verse]")
    lines.append("")
    
    for line in verse_lines:
        # Each line gets emotion/pace/vocal tags based on content
        # This is a simplified smart tagging based on content emotion
        emotion = detect_line_emotion(line)
        pace = detect_line_pace(line)
        vocal = detect_line_vocal(line, overall_emotion)
        
        if emotion:
            lines.append(f"[{emotion}]")
        if pace:
            lines.append(f"[{pace}]")
        if vocal:
            lines.append(f"[{vocal}]")
        
        lines.append(line)
        lines.append("")
    
    lines.append("")


def add_chorus(
    lines: List[str],
    chorus_lines: List[str],
    is_hook: bool = True,
) -> None:
    """Add a chorus with emphasis tagging"""
    lines.append(f"[chorus]")
    if is_hook:
        lines.append("[hook: emphasis this is the core hook]")
    lines.append("")
    
    for line in chorus_lines:
        emotion = detect_line_emotion(line)
        pace = detect_line_pace(line)
        vocal = detect_line_vocal(line, "chorus")
        
        if emotion:
            lines.append(f"[{emotion}]")
        if pace:
            lines.append(f"[{pace}]")
        if vocal:
            lines.append(f"[{vocal}]")
        
        lines.append(line)
        lines.append("")
    
    lines.append("")


def add_outro(
    lines: List[str],
    outro_lines: List[str],
    fade_out: bool = True,
) -> None:
    """Add an outro with fade out tagging"""
    lines.append(f"[outro]")
    if fade_out:
        lines.append("[fade: slow fade out]")
    lines.append("")
    
    for line in outro_lines:
        emotion = detect_line_emotion(line)
        pace = detect_line_pace(line)
        vocal = detect_line_vocal(line, "outro")
        
        if emotion:
            lines.append(f"[{emotion}]")
        if pace:
            lines.append(f"[{pace}]")
        if vocal:
            lines.append(f"[{vocal}]")
        
        lines.append(line)
        lines.append("")
    
    if fade_out:
        lines.append("[end: slow fade out, silence]")
    
    lines.append("[end]")


def detect_line_emotion(line: str) -> str:
    """Detect emotion from line content and return appropriate tag"""
    emotion_keywords = {
        "疲惫": "emotion: tired exhausted",
        "疲惫": "emotion: tired exhausted",
        "累": "emotion: tired",
        "倦": "emotion: weary",
        "快乐": "emotion: happy joyful",
        "开心": "emotion: happy",
        "悲伤": "emotion: sad melancholy",
        "难过": "emotion: sad",
        "沧桑": "emotion: vicissitudes of life, melancholy",
        "感悟": "emotion: philosophical, contemplative",
        "无奈": "emotion: helpless resignation",
        "释然": "emotion: resigned acceptance, calm",
        "温柔": "emotion: gentle soft",
        "激烈": "emotion: intense passionate",
        "愤怒": "emotion: angry intense",
        "孤独": "emotion: lonely solitary",
        "沉默": "emotion: silent contemplative",
        "微笑": "emotion: warm smiling through pain",
        "叹息": "emotion: sighing melancholy",
        "烟": "emotion: pensive smoking",
    }
    
    for keyword, tag in emotion_keywords.items():
        if keyword in line:
            return tag
    
    return ""


def detect_line_pace(line: str: str) -> str:
    """Detect pace from line content"""
    pace_keywords = {
        "慢": "pace: slow",
        "缓缓": "pace: very slow",
        "轻轻": "pace: soft slow",
        "快快": "pace: fast",
        "匆匆": "pace: hurried",
        "脚步": "pace: walking pace",
        "快跑": "pace: fast",
        "慢慢": "pace: slow",
        "停下来": "pace: stop pause",
    }
    
    for keyword, tag in pace_keywords.items():
        if keyword in line:
            return tag
    
    # Default pace based on line length
    if len(line) > 15:
        return "pace: medium"
    return ""


def detect_line_vocal(line: str, position: str) -> str:
    """Detect vocal style based on line content and position"""
    if "轻声" in line or "悄悄" in line:
        return "vocal: pianissimo, whisper"
    if "呐喊" in line or "大声" in line:
        return "vocal: forte, loud"
    if "叹息" in line:
        return "vocal: breathy, sighing"
    if position == "chorus":
        return "vocal: full voice, emotional"
    if position == "outro":
        return "vocal: fading, pianissimo"
    if "我" in line and ("说" in line or "道" in line):
        return "vocal: conversational, speaking style"
    
    return ""


def build_full_lyric(
    title: str,
    genre: str,
    style: str,
    instruments: str,
    verses: List[List[str]],
    choruses: List[List[str]],
    outro: List[str],
) -> str:
    """Build full lyric with all tags"""
    lines = []
    
    # Global tags
    lines.append(f"[title: {title}]")
    lines.append(f"[genre: {genre}]")
    lines.append(f"[instrument: {instruments}]")
    lines.append(f"[style: {style}]")
    lines.append("")
    
    # Verses and choruses
    for i, verse_lines in enumerate(verses):
        add_verse(lines, verse_lines)
    
    for i, chorus_lines in enumerate(choruses):
        add_chorus(lines, chorus_lines, is_hook=(i == len(choruses) - 1))
    
    # Outro
    add_outro(lines, outro)
    
    return "\n".join(lines)
