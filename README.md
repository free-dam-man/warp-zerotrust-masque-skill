# 最强免费VPN！Cloudflare WARP 全新复活，Zero Trust线路配置+ MASQUE协议

## —— Muse 引导式自动部署版

WARP 连不上？卡在「连接中」？速度慢得像蜗牛？

不是你的问题。是默认的 **WireGuard 协议特征太明显，被运营商干扰了**。

真正的解法只有一个动作：把设备注册进**你自己的 Cloudflare Zero Trust 团队**（免费，50 台设备，不用绑卡），再把后台设备配置文件的隧道协议从 WireGuard 换成 **MASQUE**——流量伪装成正常 HTTPS，连得上，速度还快将近一倍（原作者实测：跑满千兆、4K/8K 秒开）。

**但你不用对着教程一步步点。** 这个仓库把整套方法做成了给 AI 助手的**引导式自动化项目**：AI 一步一问、亲自操作、最后拿实测证据验收。你只做三件事：登录一次、报一次邮箱验证码、点一下连接。

---

## 两种用法

### 用法 A：引导式（推荐）——把 SKILL.md 交给你的 Muse

把本仓库的 [`SKILL.md`](SKILL.md) 作为技能/指令交给你的 AI 助手，然后说一句：

> 帮我部署 WARP Zero Trust MASQUE

它会进入 7 步向导模式：

| 步骤 | 内容 | 谁来做 |
|---|---|---|
| 第1/7步 | 确认范围：只电脑，还是电脑+手机 | 你回答 |
| 第2/7步 | 注册/登录 Cloudflare（密码不经聊天） | 你登录 |
| 第3/7步 | 定团队名称（全网唯一） | 你拍板 |
| 第4/7步 | 关掉其他 VPN/代理清场 | 你确认 |
| 第5/7步 | 建团队 → 走 6 步向导 → **改 MASQUE** | **AI 全包** |
| 第6/7步 | 客户端登录团队 + trace/测速验收 | 你报验证码，AI 验收 |
| 第7/7步 | 手机端单独建 WireGuard 配置（可选） | AI 带着走 |

### 用法 B：一次性口令——复制 PROMPT.md 整段发给 AI

不想装技能，就打开 [`PROMPT.md`](PROMPT.md)，把整段口令复制给任何能操作浏览器的 AI 助手。效果相同，一次性执行。

### 用法 C：纯手动

没有 AI 也行，照 [`docs/manual-steps.md`](docs/manual-steps.md) 的 10 步自己点，原理和坑都在里面。

---

## 三个必死的坑（先看再装）

1. **顺序反了**：必须先在后台把协议改成 MASQUE 并**保存**，再去客户端点连接。反过来要么连不上，要么慢。
2. **改错配置文件**：设备配置文件按列表顺序优先命中。改的不是设备实际命中的那份，等于白改。
3. **手机跟着用 MASQUE**：原作者博客特别提醒——手机端要**另建一份 WireGuard 协议的配置文件**，桌面 MASQUE、手机 WireGuard，双线并行。

## 验收（不用听 AI 说「好了」）

部署完在本机跑：

```bash
python3 scripts/verify_warp.py
```

它会读取 Cloudflare 官方 trace 页，告诉你 `warp` 是否启用、出口在哪个数据中心（colo）、现在的出口 IP。`warp=off` 就说明没走通，脚本会直接给出排查方向。完整排障表在 [`docs/troubleshooting.md`](docs/troubleshooting.md)。

## 项目结构

```text
.
├── SKILL.md                    # 引导式向导 + 执行手册（给 AI 看的核心文件）
├── PROMPT.md                   # 一次性口令版（复制即用）
├── docs/
│   ├── manual-steps.md         # 纯手动 10 步 + 原理
│   └── troubleshooting.md      # 排障决策树 + 回滚
├── scripts/
│   └── verify_warp.py          # 验收脚本（零依赖，Python 3 标准库）
├── NOTICE.md                   # 方法来源与商标声明
└── LICENSE                     # MIT（仅覆盖本仓库自有文本与代码）
```

## 边界（说清楚）

- 这条线出口是 Cloudflare 的网络，适合当主力/备用线路；不是匿名工具，团队账号是你自己注册的。
- 免费版 50 个席位供自己设备使用，不要公开分发或转卖，违反 Cloudflare 条款可能封号。
- 速度取决于你的宽带和运营商。本仓库不承诺任何速度数字，只要求 AI 报实测值。
- Cloudflare 后台会改版，菜单名可能微调；按功能词找：服务提供商 / 使用 WARP 注册您的设备 / 设备配置文件 / 设备隧道协议。

## 来源

部署方法来自**零度解说**，本仓库做的是逐段拆解 + AI 自动化改编：

- 原视频：《最强免费VPN！Cloudflare WARP 全新复活，Zero Trust线路配置+ MASQUE协议》 https://youtu.be/UG-l2OYdeqM
- 原作者博客图文版：https://www.freedidi.com/23223.html

详见 [NOTICE.md](NOTICE.md)。
