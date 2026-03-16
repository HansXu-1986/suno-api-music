---
name: suno-api-music
description: 基于 Suno.cn MCP 服务的全自动音乐生成，支持歌词、风格定制，通过 API 直接生成，无需网页操作，基础功能完全免费
version: 1.2.0
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
  "pro_activation_code": "",         // 🔓 基础版：留空即可 → 免费使用，限制单首生成
  "pro_activation_list_url": "",   // 👤 作者配置：公开激活码列表 Gist URL
  "default_versions": 2,
  "timeout_ms": 120000
}
```

**说明：**
- **基础版用户**：只需要填 `api_key`，`pro_activation_code` 留空 → 免费使用，限制单首生成
- **Pro 版用户**：付款后填入支付宝订单号 → 自动验证通过 → 解锁批量生成
- **作者配置**：你只需要配置一次 `pro_activation_list_url` → 自动验证，不需要你手动处理

## Pricing

- 🎉 **完全免费** - 基础功能全部可用，单首生成无限制
- 💝 **打赏解锁** - 打赏任意金额后激活批量生成（最多 10 首）
- 打赏是自愿的，基础版完全够用，感谢你的支持！

## 💰 支持开发

如果你觉得这个技能好用，欢迎打赏支持开发👇

![支付宝赞赏码]($https://pcsdata.baidu.com/thumbnail/0105b65d3hc459885de5ae19b517cfa7?fid=843748537-16051585-645516420529129&rt=pr&sign=FDTAER-yUdy3dSFZ0SVxtzShv1zcMqd-2sh4WyLvEGJkEXw3S2lFgGSAX8M%3D&expires=2h&chkv=0&chkbd=0&chkpc=&dp-logid=575398625919898124&dp-callid=0&time=1773633600&bus_no=26&size=c1600_u1600&quality=100&vuk=-&ft=video)

### 💝 打赏用户福利

打赏任意金额后，可以：
- 解锁**批量生成**功能（最多 10 首同时生成）
- 获得优先级问题支持

**激活方式：**
1. 扫码打赏
2. 复制支付宝订单号
3. 在 `config.json` 中添加：
   ```json
   {
     "sse_url": "https://mcp.suno.cn/mcp/sse",
     "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxx",
     "pro_activation_code": "你的订单号",
     "default_versions": 5,
     "timeout_ms": 120000
   }
   ```
4. ✅ 激活成功！批量生成功能已解锁

> 激活码自动验证，订单号在 Gist 列表中就能激活，作者添加后自动生效

## 💬 反馈与建议

如果你使用中遇到问题，或者有好的建议，欢迎反馈：

- 🐛 **问题报告**: [点击这里报告 Bug](https://github.com/HansXu-1986/suno-api-music/issues/new)
- 💡 **功能建议**: [点击这里提建议](https://github.com/HansXu-1986/suno-api-music/issues/new)

感谢你的反馈，帮助我们变得更好 🙏

## ⚙️ Pro 激活验证

**`suno-api-music` 内置自动验证功能，不需要依赖外部技能**

激活码验证原理：
- 作者维护一个**公开的已付款激活码列表**（放在 GitHub Gist，公开可访问）
- 用户填入激活码后，技能自动拉取列表，检查激活码是否有效
- 如果激活码在列表中 → ✅ 解锁 Pro 功能，支持批量生成（最多 10 首）
- 如果激活码不在列表中 / 为空 → ❌ 只能单首生成（基础版免费）

### 👤 用户操作步骤：
1. 扫描下方赞赏码付款 9.9 元
2. 复制支付宝订单号
3. 在 `config.json` 中添加：
   ```json
   "pro_activation_code": "你的订单号"
   ```
4. **自动验证** → 通过即解锁 Pro ✅

### 👨‍💻 作者操作方式

#### 选项一：半自动（推荐，不需要服务器，最简单）
1. 用户付款后，你支付宝收到推送通知
2. 在 OpenClaw 说一句话：
   ```
   alipay-auto-activate 添加激活码 订单号
   ```
3. ✅ **自动完成** → 订单号添加到 Gist，用户立即可用
4. 全程不需要你有服务器，只需要一句话，10 秒钟搞定

#### 选项二：全自动（需要服务器，完全不用管）
如果你有自己的服务器，可以部署 Webhook 实现**真正全自动**：

1. 部署 `webhook_server.py` 到你的服务器（或 Vercel/Render 免费托管）
2. 在支付宝商家平台配置异步通知 URL：`https://your-server.com/webhook/alipay`
3. 配置 `webhook_config.json` 填入你的 GitHub token、Gist ID、支付宝公钥
4. ✅ **完成** → 用户付款后，支付宝自动发通知 → 自动添加订单号到 Gist → 用户激活
5. **全程不需要你操作**，躺着收款就行

部署说明看 `webhook_server.py` 和 `requirements-webhook.txt`

> 使用 `alipay-auto-activate` 技能管理激活列表，两种方式都可以，选适合你的！

## Changelog

### 1.2.0 (2026-03-16)
- 🎉 Changed to donation model: base version is fully free, donation unlocks batch generation
- 💝 All core features are free, donation is voluntary
- Keep automatic activation verification for donation users

### 1.1.1 (2026-03-16)
- ✨ Add optional full automatic webhook server for zero-configuration activation
- ✨ Support both semi-auto (no server) and full-auto (with server)

### 1.1.0 (2026-03-16)
- ✨ **Integrated automatic Pro activation directly in the skill**
- ✨ Add `pro_activation.py` with built-in verification function
- ✨ Users fill order number in config → skill auto-verify from Gist → unlock Pro
- ✨ Use `alipay-auto-activate` for easy activation code management (no server needed)
- ✅ `pro_activation_list_url` pre-configured with your Gist

### 1.0.5 (2026-03-16)
- ✨ Add automatic Pro activation with public Gist verification
- ✨ Add strict activation code checking
- Add alipay-auto-activate integration

### 1.0.4 (2026-03-16)
- ✨ Fix: pro_activation_code is optional, base version doesn't require payment
- 🐛 Fix configuration example

### 1.0.3 (2026-03-16)
- ✨ Add strict pro activation verification with public gist list
- ✨ Automatic validation

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
