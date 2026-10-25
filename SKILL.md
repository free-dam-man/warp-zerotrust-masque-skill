---
name: warp-zerotrust-masque
description: "Guided, Muse-operated deployment of Cloudflare WARP on a personal Zero Trust team with the MASQUE tunnel protocol. Use when someone says WARP won't connect, WARP is stuck on connecting, WARP is slow, or asks to set up / deploy / fix Cloudflare WARP, Zero Trust WARP, or the MASQUE protocol, step by step with the AI doing the work. 中文触发词: WARP连不上, WARP连接中, Zero Trust配置, MASQUE切换, 免费VPN部署."
---

# WARP Zero Trust + MASQUE — Guided Auto-Deployment

You (the AI agent) deploy this for the operator. The operator is usually
non-technical: they only log in, read out one email code, and tap Connect.
Every other step is yours: browser work, settings, verification, reporting.

Goal state: the operator's device(s) are enrolled in **their own**
Cloudflare Zero Trust team (Free plan, 50 seats), the desktop device
profile's tunnel protocol is **MASQUE**, the WARP client is logged in to
that team and connected, and you have *evidence* for each claim.

Method credit: the underlying manual method (Zero Trust team + MASQUE
switch) is by 零度解说 — video https://youtu.be/UG-l2OYdeqM and blog
https://www.freedidi.com/23223.html . This skill turns that method into a
guided, agent-executed flow. Mention the source once in your final report.

## Iron rules (never break)

1. **Evidence before statement.** Never say "done / connected / fast"
   without a real observed result behind it: a settings value you read
   back, a trace result, a measured speed. Fluency is not truth.
2. **No credentials in chat.** The operator logs in inside the browser
   themselves. Never ask for a password. The email one-time code is read
   out by the operator, or read by you from their mailbox only after they
   explicitly agree in this session.
3. **Never add a payment method.** The Free plan works without one; at
   the billing step you exit via Cancel (step S3). If the UI offers no
   exit and demands payment details, STOP and report — do not improvise.
4. **Do not clobber an existing setup.** If the operator already has a
   Cloudflare account or a Zero Trust team, report what exists first.
   Never overwrite or delete an existing device profile; create/edit only
   with the operator's confirmation, and prefer editing the profile the
   wizard just created for this deployment.
5. **One question at a time.** In the wizard below, ask exactly one
   question, wait for the answer, validate it, then move on.
6. **Speed is measured, never promised.** The original author's demo
   reached 600 Mbps+ and smooth 8K on *his* gigabit line. Report only the
   operator's own measured numbers.

## Guided wizard (default mode)

Before step 1, send the operator this heads-up card verbatim, as one
message, before asking anything:

```text
先花30秒看完, 然后我们一步一步来:
一共7步, 每步我只问一句, 你回一句就行, 配置的活我来做, 不用你动手。
必需: 一个邮箱(注册 Cloudflare 用, Google/Apple 账号也行)。
不用绑卡、不用付费: 免费版 50 台设备, 付款页面我们直接跳过。
你要做的只有三件事: 1) 在浏览器里登录一次, 2) 报一次邮箱验证码, 3) 最后点一下连接。
核心动作只有一个: 把默认的 WireGuard 协议换成 MASQUE——这是 WARP 连不上、速度慢的真正原因。
预计耗时: 通常十几分钟, 主要取决于注册验证和你的回复速度, 不保证固定时间。
速度以最后实测为准, 我测出来多少就报多少, 不提前承诺。
```

Every wizard question starts with the prefix `第X/7步`. Follow-ups inside
the same step keep the same prefix.

- **W1 Scope — 第1/7步.** Ask: "第1/7步: 只装这台电脑, 还是电脑 + 手机都要? 回 1(只电脑) 或 2(电脑+手机)。"
  Record the choice; it decides whether W7 runs.
- **W2 Account — 第2/7步.** Ask: "第2/7步: 你有 Cloudflare 账号吗? 没有的话打开 dash.cloudflare.com 用邮箱注册一个(免费), 有的话直接登录。登录好回我一句 好了 。登录和验证请你在浏览器里自己完成, 密码不用发我。"
  Wait for confirmation. If sign-up hits email verification, coach them
  to click the link in their mailbox, then confirm.
- **W3 Team name — 第3/7步.** Ask: "第3/7步: 给你的团队起个名字: 小写英文/数字, 全网唯一, 比如 yourname2026。想不出来回 想不出 , 我给你 3 个候选你挑。"
  Validate format (lowercase letters, digits, hyphens). Explain this
  becomes `<team>.cloudflareaccess.com` and is needed later at client
  login. If Cloudflare later rejects it as taken, append digits and
  re-confirm with the operator.
- **W4 Clear the deck — 第4/7步.** Ask: "第4/7步: 先把电脑上其他 VPN / 代理全关掉(包括旧的 WireGuard 客户端), 两个隧道会互相抢流量, 不关后面必定连不上。关好回我 好了 。"
  Do not proceed on a vague answer; this is the #1 cause of failure.
- **W5 Backend build — 第5/7步 (you execute).** Tell them: "第5/7步: 接下来我来配置后台, 中间不用你操作, 完事我汇报。" Then run
  playbook S3–S6 below (team creation, free plan, wizard, MASQUE switch).
  Report each milestone in one short line as you finish it. Do NOT ask
  the operator to click anything in this step.
- **W6 Login + verify — 第6/7步.** Guide the client login (playbook S7):
  when the email code is sent, ask: "第6/7步: 验证码发到你邮箱了(10 分钟内有效), 打开邮箱把 6 位数字报给我, 或者你自己填进客户端也行。"
  After login, run S8 verification yourself where possible (open the
  trace page in the browser / run `scripts/verify_warp.py` on the
  machine) and report measured results.
- **W7 Phone (only if W1 = 2) — 第7/7步.** Walk the phone flow in S9.
  Emphasize the split: desktop profile = MASQUE, phone profile =
  WireGuard (a separate device profile). Verify the phone connects
  before declaring done. If W1 = 1, say "第7/7步: 你选了只装电脑, 手机端跳过。以后想加, 随时喊我。"

## Execution playbook (the work behind the wizard)

- **S1 Environment.** Confirm OS. Confirm other VPN/proxy tools are off
  (W4). Check whether a WARP client is already installed.
- **S2 Login.** Operator logs in at dash.cloudflare.com (sign-up:
  email / Google / Apple). Onboarding survey: choose personal use, skip
  the rest. Language can be switched via avatar → Language.
- **S3 Create the Zero Trust team.** Left nav → Zero Trust → Get started
  → set the W3 team name → choose the **Free** plan (0, 50 seats) → at
  the payment-method page choose **Cancel and exit / Confirm and exit**
  without entering any payment details → return and confirm the team now
  exists in Zero Trust. Record the full team domain
  `<team>.cloudflareaccess.com`.
- **S4 Device enrollment entry.** Zero Trust → Integrations/Settings →
  Service providers → "Enroll your device with WARP" (使用 WARP 注册您的
  设备) → Add a device → the official setup wizard opens.
- **S5 The 6-step wizard (accept defaults except where stated).**
  1. Download WARP: latest stable client for the operator's OS
     (Windows build is ~130 MB); install it.
  2. Define the enrollment policy: default — allow the operator's
     sign-in email to enroll devices.
  3. Service mode: choose the FIRST option, **Gateway with WARP —
     traffic + DNS** (dual channel, most stable).
  4. Default route: **Exclude mode** (all traffic via Cloudflare except
     listed exceptions).
  5. Split tunnel: keep defaults, continue.
  6. Finish WARP installation.
- **S6 THE critical step — switch the tunnel protocol BEFORE anyone
  connects.** Zero Trust → Teams & Resources (团队和资源) → Devices
  (设备) → **Device profiles** tab (设备配置文件) → find the profile the
  wizard just created AND that the device actually matches — profiles
  are evaluated in list order, first match wins → `⋯` menu → Configure
  (配置) → scroll to the bottom: **Device tunnel protocol** (设备隧道
  协议) → change **WireGuard → MASQUE** (the second option) → confirm
  the dialog → scroll down → **Save profile** (保存配置文件). Then
  re-open the profile and read the value back: it must say MASQUE.
- **S7 Client login.** System tray WARP icon → gear (Settings) →
  Preferences → Account → **Log in with Cloudflare Zero Trust** → enter
  the team name from S3 → enter the account email → enter the emailed
  one-time code (sender: Cloudflare; valid 10 minutes) → the client now
  shows the Zero Trust team. Do not connect yet if S6 is unfinished.
- **S8 Connect + verify (all four, with evidence).**
  1. Click Connect → client shows Connected / traffic protected.
  2. Open https://www.cloudflare.com/cdn-cgi/trace — `warp` must not be
     `off` (enabled shows `on` or `gateway`); report the `colo`.
     (On the target machine you can also run `scripts/verify_warp.py`.)
  3. An IP-lookup page shows a Cloudflare egress IP (e.g. 104.18.x.x).
  4. Run a speed test and play a 4K video; report the measured numbers
     verbatim. No promised speeds (rule 6).
- **S9 Phone (W7).** Install the **Cloudflare One Agent** app (Cloudflare's current dedicated Zero Trust client, also what the author's blog recommends; the video demo used the older *1.1.1.1* app, whose Zero Trust support Cloudflare has officially ended on mobile) → Next → Accept → notifications either
  way → top-right hamburger menu → Account → Log in with Cloudflare
  Zero Trust → same team name → email code login → Connect.
  **Author's explicit warning:** do NOT reuse the desktop MASQUE
  profile for the phone. Create a SEPARATE device profile with tunnel
  protocol **WireGuard** that matches the phone; keep the desktop on
  MASQUE. If the phone fails under MASQUE, do not retry in circles —
  build the WireGuard profile and retest.

## Troubleshooting ( symptom → cause → fix )

| Symptom | Likely cause | Fix |
|---|---|---|
| Stuck on "Connecting" forever | Still on default WireGuard, carrier blocks/throttles it | S6: switch the *matching* profile to MASQUE and Save |
| MASQUE set but still can't connect | Edited the wrong profile (list order = priority) | Check profile order/match; edit the one the device actually matches |
| One device fine, another broken | Another VPN/proxy still running on the broken one | Quit all other VPN/proxy/old WireGuard clients, reconnect |
| Phone won't connect | Phone matched the MASQUE profile | Separate WireGuard profile for the phone (S9) |
| No code email | Wrong email / spam folder / code expired (10 min) | Verify email, check spam, resend once |
| Team name rejected | Taken (globally unique) | Append digits/suffix, re-confirm with operator |
| Stuck at payment page | Free plan doesn't need a card | Cancel and exit; features keep working (author-verified) |
| Connected but slow | Distant colo, or MASQUE not actually saved | Re-read profile value; check `colo` in trace; reconnect once |
| Old account already has Zero Trust | No re-registration needed | Just do S6 on the existing team's matching profile |

## Final delivery checklist (report exactly this)

- [ ] Team name + team domain (`<team>.cloudflareaccess.com`)
- [ ] Account email used (operator's own)
- [ ] Plan: Free, no payment method added
- [ ] Desktop profile name + tunnel protocol read back = MASQUE
- [ ] Phone profile name + protocol = WireGuard (if phone included)
- [ ] Client state: Connected; trace `warp` value + `colo`; egress IP
- [ ] Measured speed (operator's own test, with the number)
- [ ] Rollback: client Account → log out of Zero Trust; or set the
      profile's tunnel protocol back to WireGuard and Save
- [ ] Source credited: method by 零度解说 (video + blog links above)

## Boundaries

- This line exits via Cloudflare's network; it is a convenience/backup
  connection, not an anonymity tool. Say so once, plainly.
- The 50 free seats are for the operator's own devices. No public
  sharing or resale; that risks the account under Cloudflare's terms.
- Cloudflare renames dashboard menus over time. Navigate by functional
  labels — Service providers / Enroll device with WARP / Device profiles
  / Device tunnel protocol — not by memorized coordinates.
