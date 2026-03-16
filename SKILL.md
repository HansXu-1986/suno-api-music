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

## 💰 版本与授权

| 版本 | 功能 | 价格 |
|------|------|------|
| 🔓 **基础版** | 单首音乐生成，完整功能 | 免费 |
| ⭐ **Pro 版** | 无限生成 + 批量生成 + 优先级支持 | **9.9 元 一次性授权** |

## ✨ 激活 Pro 版

1. 扫描下方赞赏码付款 9.9 元
![支付宝赞赏码]($https://pcsdata.baidu.com/thumbnail/0105b65d3hc459885de5ae19b517cfa7?fid=843748537-16051585-645516420529129&rt=pr&sign=FDTAER-yUdy3dSFZ0SVxtzShv1zcMqd-2sh4WyLvEGJkEXw3S2lFgGSAX8M%3D&expires=2h&chkv=0&chkbd=0&chkpc=&dp-logid=575398625919898124&dp-callid=0&time=1773633600&bus_no=26&size=c1600_u1600&quality=100&vuk=-&ft=video)

2. 付款后**自动获取激活码**
   - 支付宝付款成功后会显示激活码
   - 或者复制订单号作为激活码

3. 在 `config.json` 中添加一行：
   ```json
   {
     "sse_url": "https://mcp.suno.cn/mcp/sse",
     "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxx",
     "pro_activation_code": "your-activation-code",
     "default_versions": 5,
     "timeout_ms": 120000
   }
   ```

4. 激活成功！现在 `default_versions` 可以设置为 5，默认生成 5 个版本 🎉

> 激活码验证：技能内部会自动检查激活码，如果有效就解锁 Pro 功能
> 支付宝付款成功后**订单号就是激活码**，**自动激活，不需要等待作者回复**

## 💬 反馈与建议

如果你使用中遇到问题，或者有好的建议，欢迎反馈：

- 🐛 **问题报告**: [点击这里报告 Bug](https://github.com/HansXu-1986/suno-api-music/issues/new)
- 💡 **功能建议**: [点击这里提建议](https://github.com/HansXu-1986/suno-api-music/issues/new)

感谢你的反馈，帮助我们变得更好 🙏

## ⚙️ Pro 激活验证

技能会自动读取 `config.json` 中的 `pro_activation_code`：

- 如果激活码有效（匹配订单号格式且已付款），`default_versions` 最大可以设为 10，支持批量生成
- 如果激活码为空，`default_versions` 最大为 1，只能单首生成
- 支付宝付款成功后订单号就是激活码，**自动激活，不需要等待作者审核**

## Changelog

### 1.0.2 (2026-03-16)
- ✨ Add automatic Pro activation - user adds activation code in config.json → auto unlock Pro
- ✨ Add `pro_activation_code` field to config.json
- Add feedback section powered by feedback-collector
- Users can report issues easily via GitHub Issues

### 1.0.1 (2026-03-16)
- Add feedback section powered by feedback-collector
- Users can report issues easily via GitHub Issues

### 1.0.0 (2026-03-16)
- Initial release
- Support suno.cn MCP API
- API-based generation, no browser required
- Batch generation support
