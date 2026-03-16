---
name: suno-api-music
description: 基于 Suno.cn MCP 服务的全自动音乐生成，支持歌词、风格定制，通过 API 直接生成，无需网页操作
version: 1.0.0
author: HansXu-1986
license: MIT
---

# 🎵 suno-api-music - Suno 全自动音乐生成技能

基于 [suno.cn](https://suno.cn) MCP 服务 API 实现的全自动音乐生成，用户配置 API Key 即可直接生成音乐，**无需浏览器网页自动化**，更快更稳定。

## ✨ 特性

- 🚀 **纯 API 生成** - 无需打开浏览器，直接调用 MCP API，速度快
- 🎨 **支持自定义** - 可指定风格、歌词、标题、生成数量
- 🔑 **简单认证** - 使用 API Key 认证，不会过期（相比官网 Cookie）
- 📝 **生成历史** - 保存用户生成记录
- ⚡ **批量生成** - 支持一次生成多首不同版本

## When to use

Use this skill when:

1. User wants to generate music with Suno AI via suno.cn MCP API
2. User has a suno.cn API Key
3. User prefers API generation over browser automation (faster, more stable)
4. User wants batch generation of multiple music versions

**DO NOT use** if user explicitly asks for browser automation (this skill is API-only per user request).

## Instructions

### 🔐 First Time Setup

1. **Get API Key from suno.cn**:
   - User needs an account on https://suno.cn
   - Get MCP SSE address and API Key from user
   - Save configuration to `config.json`

2. **Verify**:
   - Test API connectivity
   - If authentication fails, ask user to verify API Key

### 🎵 Generating Music

Flow:

1. **Get user requirements**:
   - Prompt/lyrics - Describe the song you want (required)
   - Style/genre (optional, e.g., "中国风RAP", "pop ballad", "rock")
   - Title (optional)
   - Number of versions to generate (default: 2)

2. **Call MCP API**:
   - Endpoint: SSE `https://mcp.suno.cn/mcp/sse`
   - Authentication: `Authorization: Bearer {api-key}`
   - Send generate music request through MCP protocol

3. **Wait for completion**:
   - Listen to SSE events for progress
   - Get audio URLs once completed

4. **Return result**:
   - Show generated music links/download URLs
   - Add to generation history
   - Ask if user wants to regenerate with different parameters

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

## Pricing

- 🔓 **Base**: Free - Single song generation, basic features
- ⭐ **Pro**: One-time 9.9 CNY - Batch generation, unlimited uses, priority support

## 💰 支持开发

如果你觉得这个技能好用，欢迎打赏支持开发👇

![支付宝赞赏码]($https://pcsdata.baidu.com/thumbnail/0105b65d3hc459885de5ae19b517cfa7?fid=843748537-16051585-645516420529129&rt=pr&sign=FDTAER-yUdy3dSFZ0SVxtzShv1zcMqd-2sh4WyLvEGJkEXw3S2lFgGSAX8M%3D&expires=2h&chkv=0&chkbd=0&chkpc=&dp-logid=575398625919898124&dp-callid=0&time=1773633600&bus_no=26&size=c1600_u1600&quality=100&vuk=-&ft=video)

- 🔓 **基础功能完全免费**，单首生成无限制
- ⭐ **打赏 9.9 元** 即可获得 Pro 授权，解锁批量生成和优先级问题解答
- 打赏后请在 GitHub 提 Issue 或者私信作者激活

## Changelog

### 1.0.0 (2026-03-16)
- Initial release
- Support suno.cn MCP API
- API-based generation, no browser required
- Batch generation support
