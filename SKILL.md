---
name: suno-api-music
description: 基于 Suno.cn MCP 服务的全自动音乐生成，支持歌词、风格定制，通过 API 直接生成，无需网页操作，两种生成模式（自动一句话/自定义分步），完全免费
version: 1.6.0
author: HansXu-1986
license: MIT
---

# 🎵 suno-api-music - Suno 全自动音乐生成技能

基于 [suno.cn](https://suno.cn) MCP 服务 API 实现的全自动音乐生成，**纯 API 调用，不需要网页自动化**，更快更稳定，完全免费使用。

## ✨ 特性

- 🚀 **纯 API 生成** - 无需打开浏览器，直接调用 MCP API，速度快
- 🎨 **两种生成模式**:
  - **自动模式** - 一句话描述 → 直接生成，简单快捷
  - **自定义模式** - 分步询问 → 预览确认 → 生成，精准控制
- 🎯 **高度自定义** - 可指定风格、歌词、标题、生成数量、纯音乐
- 📝 **预览确认** - 自定义模式生成歌词预览，带完整元标签和分段，确认后再生成
- 🔑 **简单认证** - 使用 API Key 认证，不会过期（相比官网 Cookie）
- 📝 **生成历史** - 保存用户生成记录
- ⚡ **批量生成** - 支持一次生成最多 10 个不同版本
- 🎁 **完全免费** - 所有功能全开，自愿赞赏

## When to use

Use this skill when:

1. You want to generate music with Suno AI via suno.cn MCP API
2. You have a suno.cn API Key
3. You prefer API generation over browser automation (faster, more stable)
4. You want either quick auto generation or full custom control with preview

**DO NOT use** browser automation - this skill is pure API per explicit requirement.

## 🎨 风格参考 (from suno.cn official guide)

根据 suno.cn 官方指南，这里是常用风格参考：

### 常见音乐风格分类

**流行 Pop**
- 流行民谣 Pop Folk
- 流行摇滚 Pop Rock
- synth-pop 合成器流行
- power-pop 力量流行

**摇滚 Rock**
- 硬摇滚 Hard Rock
- 另类摇滚 Alternative Rock
- 英伦摇滚 Britpop
- 朋克 Punk
- 金属 Metal

**民谣 Folk**
- 美国民谣 American Folk
- 现代民谣 Contemporary Folk
- 民谣摇滚 Folk Rock
- 乡村民谣 Country Folk

**说唱 Rap/Hip Hop**
- 东岸说唱 East Coast Rap
- 西岸说唱 West Coast Rap
- 嘻哈 Hip Hop
- Trap

**电子 Electronic**
- 电子舞曲 EDM
- 合成器 Synth
- 氛围电子 Ambient
- 科技舞曲 Techno

**爵士 Jazz**
- 冷爵士乐 Cool Jazz
- 比波普 Bebop
- 融合爵士 Fusion Jazz
- 顺滑爵士 Smooth Jazz

### 正确写法提示

在歌词预览中使用官方标签格式：
```
[genre: 民谣]
[style: 娓娓道来, 抒情走心]
[instrument: 木吉他, 口琴, 轻鼓点]

[verse]
四十岁的清晨 闹钟响第三遍
...

[chorus]
四十还在惑 未来是什么
...
```

## Instructions

### 🔐 First Time Setup

1. **Get API Key from suno.cn**:
   - You need an account on https://suno.cn
   - Get MCP SSE address and API Key
   - Save configuration to `config.json`

2. **Configuration**:

```json
{
  "sse_url": "https://mcp.suno.cn/mcp/sse",
  "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxx",
  "default_versions": 2,
  "timeout_ms": 120000
}
```

That's it! No activation required, everything is free.

### 🎵 Generating Music

Two generation modes:

#### 1. 🚀 Auto Mode (Recommended)
Just describe what song you want in one sentence, we generate directly:
> "帮我生成一首轻快的民谣，主题：春天花开"

- ✅ Simple and fast
- ✅ AI handles everything automatically

#### 2. 🎨 Custom Mode (Full control)
Step-by-step inquiry, you control every detail:
1. You say "custom mode" or "自定义模式"
2. We ask you step by step:
   - Theme/lyrics
   - Style/genre
   - Title
   - Full lyrics (optional)
   - Instrumental only?
   - Number of versions
3. We **generate full preview**:
   - Complete metadata tags: `[title] [genre] [instrument]`
   - Lyrics preview with `[verse]/[chorus]/[outro]` section tags
   - You see everything before generating
4. You confirm all information
5. We generate after confirmation

- ✅ Full control over every detail
- ✅ Preview with complete metadata before generation
- ✅ You can check and adjust before sending to Suno

### Flow:

After you confirm all parameters:

1. **Call MCP API**:
   - Endpoint: SSE `https://mcp.suno.cn/mcp/sse`
   - Authentication: `Authorization: Bearer {api-key}`
   - Send generate music request through MCP protocol

2. **Wait for completion**:
   - Listen to SSE events for progress
   - Get audio URLs once completed

3. **Return result**:
   - Show generated music links/download URLs
   - Add to generation history

### ⚠️ Error Handling

- 401 Unauthorized: API Key invalid → Ask user to check API Key
- Rate limit hit → Wait and retry, or ask user to wait
- Service unavailable → Inform user and suggest trying again later

## API Endpoints (as of 2026-03)

- SSE Endpoint: `https://mcp.suno.cn/mcp/sse`
- Authentication: HTTP Header `Authorization: Bearer {API_KEY}`

## Configuration

Store in `config.json`:

```json
{
  "sse_url": "https://mcp.suno.cn/mcp/sse",
  "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxx",
  "default_versions": 2,
  "timeout_ms": 120000
}
```

## 💎 完全免费

**suno-api-music 完全免费，所有功能都可以用！**

- ✅ 单首生成免费
- ✅ 批量生成免费（最多 10 首）
- ✅ 自定义模式免费
- ✅ 所有功能全开

如果你觉得这个技能好用，欢迎扫码赞赏支持开发 👇

![支付宝赞赏码](https://pcsdata.baidu.com/thumbnail/0105b65d3hc459885de5ae19b517cfa7?fid=843748537-16051585-645516420529129&rt=pr&sign=FDTAER-yUdy3dSFZ0SVxtzShv1zcMqd-2sh4WyLvEGJkEXw3S2lFgGSAX8M%3D&expires=2h&chkv=0&chkbd=0&chkpc=&dp-logid=575398625919898124&dp-callid=0&time=1773633600&bus_no=26&size=c1600_u1600&quality=100&vuk=-&ft=video)

感谢你的支持！

## 💬 反馈与建议

如果你使用中遇到问题，或者有好的建议，欢迎反馈：

- 🐛 **问题报告**: [点击这里报告 Bug](https://github.com/HansXu-1986/suno-api-music/issues/new)
- 💡 **功能建议**: [点击这里提建议](https://github.com/HansXu-1986/suno-api-music/issues/new)

感谢你的反馈，帮助我们变得更好 🙏

## Changelog

### 1.6.0 (2026-03-16)
- ✨ **Advanced lyric generation with per-line detailed tagging**:
- ✨ Each lyric line gets automatic emotion/pace/vocal tags based on content
- ✨ Full metadata tagging: global + per-line for maximum richness
- ✨ Follows suno.cn official prompt specification exactly
- ✨ Generates deeply textured prompts that Suno can understand perfectly

### 1.5.0 (2026-03-16)
- 🎉 Completely free - all features unlocked, no activation required
- ✨ Removed activation verification, everyone can use batch generation for free
- ✨ All functions are available for free, donation is voluntary

### 1.4.0 (2026-03-16)
- ✨ **Complete preview for custom mode**:
- ✨ Generate lyrics preview with metadata tags before generation
- ✨ Add `[title] [genre] [instrument]` meta tags
- ✨ Add `[verse] [chorus] [outro]` section tags for lyrics
- ✨ User can preview everything before confirming generation

### 1.3.0 (2026-03-16)
- ✨ **Add two generation modes**:
  - 🚀 Auto mode: one sentence → generate directly, simple and fast
  - 🎨 Custom mode: step-by-step inquiry, confirm before generation, full control
- ✨ User can choose mode freely, better user experience

### 1.2.0 (2026-03-16)
- 🎉 Changed to donation model: base version is fully free, donation unlocks batch generation
- 💝 All core features are free, donation is voluntary
- Keep automatic activation verification for donation users

### 1.1.0 (2026-03-16)
- ✨ **Integrated automatic Pro activation directly in the skill**
- ✨ Add `pro_activation.py` with built-in verification function
- ✨ Users fill order number in config → skill auto-verify from Gist → unlock Pro
- ✨ Use `alipay-auto-activate` for easy activation code management (no server needed)
- ✅ `pro_activation_list_url` pre-configured with your Gist

### 1.0.0 (2026-03-16)
- Initial release
- Support suno.cn MCP API
- API-based generation, no browser required
- Batch generation support
