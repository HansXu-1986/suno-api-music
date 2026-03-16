#!/usr/bin/env python3
"""
Chinese lyric utilities: Rhyme, tone, context, rhetoric
Uses pypinyin for accurate pinyin conversion
STRICT RHYMING: exact final match, not just 十三辙 broad category
Supports:
- Accurate Chinese rhyme detection (strict final matching)
- Tone matching (ping ze)
- Rhetorical devices
- Writing techniques for song lyrics
"""

from typing import List, Dict, Tuple, Optional
import re
from pypinyin import pinyin, Style

# Strict rhyme grouping by exact final (no merging an/ian/uan)
# Strict = every final is its own group
STRICT_RHYME_GROUPS = {
    "a": ["a"],
    "ia": ["ia"],
    "ua": ["ua"],
    "o": ["o"],
    "uo": ["uo"],
    "e": ["e"],
    "ie": ["ie"],
    "üe": ["üe"],
    "i": ["i"],
    "er": ["er"],
    "u": ["u"],
    "-i": ["-i"],
    "ü": ["ü"],
    "ai": ["ai"],
    "uai": ["uai"],
    "ei": ["ei"],
    "ui": ["ui"],
    "ao": ["ao"],
    "iao": ["iao"],
    "ou": ["ou"],
    "iu": ["iu"],
    "an": ["an"],
    "ian": ["ian"],
    "uan": ["uan"],
    "üan": ["üan"],
    "en": ["en"],
    "in": ["in"],
    "un": ["un"],
    "ün": ["ün"],
    "ang": ["ang"],
    "iang": ["iang"],
    "uang": ["uang"],
    "eng": ["eng"],
    "ing": ["ing"],
    "ueng": ["ueng"],
    "ong": ["ong"],
    "iong": ["iong"],
}

# Strict matching: exact final must match
FINAL_TO_STRICT_GROUP = {final: final for final in STRICT_RHYME_GROUPS.keys()}


def get_final(pinyin_str: str) -> Optional[str]:
    """Extract final from pinyin string"""
    # Remove tone number
    pinyin_str = re.sub(r'\d+$', '', pinyin_str)
    
    # Find the longest matching final
    finals = sorted(FINAL_TO_STRICT_GROUP.keys(), key=len, reverse=True)
    for final in finals:
        if pinyin_str.endswith(final):
            return final
    return None


def get_rhyme_group(char: str, strict: bool = True) -> Optional[str]:
    """Get rhyme group for a single Chinese character"""
    if not char or not ('\u4e00' <= char <= '\u9fff'):
        return None
    
    # Get pinyin for the character
    py = pinyin(char, style=Style.TONE3, heteronym=False)
    if not py or not py[0]:
        return None
    
    pinyin_str = py[0][0]
    final = get_final(pinyin_str)
    
    if final in FINAL_TO_STRICT_GROUP:
        return FINAL_TO_STRICT_GROUP[final]
    
    return None


def do_rhyme_match(char1: str, char2: str, strict: bool = True) -> bool:
    """Check if two characters rhyme (exact same final for strict)"""
    rg1 = get_rhyme_group(char1, strict)
    rg2 = get_rhyme_group(char2, strict)
    
    if rg1 is None or rg2 is None:
        return False
    
    return rg1 == rg2


def check_lines_rhyme(lines: List[str], rhyme_scheme: str = "aabb", strict: bool = True) -> List[Tuple[int, int, str]]:
    """
    Check if lines rhyme according to scheme
    Returns list of mismatches
    """
    mismatches = []
    lines = [line.strip() for line in lines if line.strip()]
    
    if len(lines) < 2:
        return mismatches
    
    if rhyme_scheme == "aabb":
        # Line 1 rhymes with 2, line 3 rhymes with 4
        if len(lines) >= 2:
            c1 = lines[0][-1]
            c2 = lines[1][-1]
            if not do_rhyme_match(c1, c2, strict):
                rg1 = get_rhyme_group(c1, strict) or "unknown"
                rg2 = get_rhyme_group(c2, strict) or "unknown"
                mismatches.append((0, 1, f"第1、2句不押韵：'{c1}'({rg1}) vs '{c2}'({rg2})"))
        
        if len(lines) >= 4:
            c3 = lines[2][-1]
            c4 = lines[3][-1]
            if not do_rhyme_match(c3, c4, strict):
                rg3 = get_rhyme_group(c3, strict) or "unknown"
                rg4 = get_rhyme_group(c4, strict) or "unknown"
                mismatches.append((2, 3, f"第3、4句不押韵：'{c3}'({rg3}) vs '{c4}'({rg4})"))
    
    elif rhyme_scheme == "abab":
        if len(lines) >= 4:
            c1 = lines[0][-1]
            c3 = lines[2][-1]
            if not do_rhyme_match(c1, c3, strict):
                rg1 = get_rhyme_group(c1, strict) or "unknown"
                rg3 = get_rhyme_group(c3, strict) or "unknown"
                mismatches.append((0, 2, f"第1、3句不押韵：'{c1}'({rg1}) vs '{c3}'({rg3})"))
            
            c2 = lines[1][-1]
            c4 = lines[3][-1]
            if not do_rhyme_match(c2, c4, strict):
                rg2 = get_rhyme_group(c2, strict) or "unknown"
                rg4 = get_rhyme_group(c4, strict) or "unknown"
                mismatches.append((1, 3, f"第2、4句不押韵：'{c2}'({rg2}) vs '{c4}'({rg4})"))
    
    elif rhyme_scheme == "aaaa":
        # All lines rhyme
        if len(lines) <= 1:
            return mismatches
        first_char = lines[0][-1]
        first_rg = get_rhyme_group(first_char, strict)
        for i, line in enumerate(lines[1:], 1):
            char = line[-1]
            rg = get_rhyme_group(char, strict)
            if rg != first_rg:
                mismatches.append((0, i, f"第{i+1}句不押韵：'{char}'({rg}) vs '{first_char}'({first_rg})"))
    
    return mismatches


def get_tone(char: str) -> Optional[int]:
    """Get tone (1-5) for character"""
    # 1: 阴平 (ˉ) ping
    # 2: 阳平 (ˊ) ping  
    # 3: 上声 (ˇ) ze
    # 4: 去声 (ˋ) ze
    # 5: 轻声 ze
    if not char or not ('\u4e00' <= char <= '\u9fff'):
        return None
    
    py = pinyin(char, style=Style.TONE3, heteronym=False)
    if not py or not py[0]:
        return None
    
    pinyin_str = py[0][0]
    match = re.search(r'(\d)$', pinyin_str)
    if match:
        return int(match.group(1))
    
    return 5  #轻声


def is_ping(char: str) -> bool:
    """Check if character is ping tone (阴平, 阳平)"""
    tone = get_tone(char)
    if tone is None:
        return True  # default
    return tone in [1, 2]


def is_ze(char: str) -> bool:
    """Check if character is ze tone (上声, 去声, 轻声)"""
    return not is_ping(char)


def check_line_tone(line: str, expected_end: str = None) -> Dict:
    """Check tone of line ending"""
    if not line.strip():
        return {"ping": False, "ze": False, "matches_expected": None}
    
    last_char = line.strip()[-1]
    ping = is_ping(last_char)
    
    if expected_end is None:
        return {"ping": ping, "ze": not ping, "matches_expected": None}
    
    expected_ping = expected_end == "ping"
    matches = (ping == expected_ping)
    
    return {"ping": ping, "ze": not ping, "matches_expected": matches}


def validate_lyric(verses: List[List[str]], rhyme_scheme: str = "aabb", strict: bool = True) -> Dict:
    """Validate entire lyric for rhyme, tone, structure"""
    issues = []
    total_lines = 0
    total_mismatches = 0
    
    for i, verse in enumerate(verses):
        verse_clean = [line.strip() for line in verse if line.strip()]
        mismatches = check_lines_rhyme(verse_clean, rhyme_scheme, strict)
        for mismatch in mismatches:
            issues.append(f"第 {i+1} 段：{mismatch[2]}")
        total_mismatches += len(mismatches)
        total_lines += len(verse_clean)
    
    score = 100
    if total_lines > 0:
        score = 100 - (total_mismatches * (100 // total_lines))
    
    return {
        "total_lines": total_lines,
        "total_mismatches": total_mismatches,
        "issues": issues,
        "score": max(0, score),
        "perfect": total_mismatches == 0,
    }


def find_rhyming_words(target_char: str, word_list: List[str], strict: bool = True) -> List[str]:
    """Find words in word_list that rhyme with target_char"""
    result = []
    target_rg = get_rhyme_group(target_char, strict)
    if target_rg is None:
        return result
    
    for word in word_list:
        if not word:
            continue
        last = word[-1]
        rg = get_rhyme_group(last, strict)
        if rg == target_rg:
            result.append(word)
    
    return result
