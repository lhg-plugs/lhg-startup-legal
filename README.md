<!-- About 简介（推送后填写到仓库 About 栏）：
创业法务助手：公司类型选择→注册流程清单→股权结构设计→核心协议清单；非律师意见、仅供参考，重要事项请咨询执业律师。 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-startup-legal
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, startup-legal, company-registration, equity-design, cap-table, contracts -->

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="lhg-startup-legal — 创业法务助手">
</p>

> **一句话介绍**：创业法务助手：公司类型选择→注册流程清单→股权结构设计→核心协议清单；非律师意见、仅供参考，重要事项请咨询执业律师。

**一键安装**：在 Claude Code 里运行

```bash
/plugin marketplace add lhg-plugs/lhg-startup-legal
/plugin install lhg-startup-legal@lhg-plugs
```

## 它能帮你做出什么

- **冒烟全绿**：`python3 smoke_test.py` 48 项全部通过（JSON 合法、frontmatter 完整、命令/skill/agent 齐全）。

## 它是什么

`lhg-startup-legal` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **3 个命令**（小白入口）：`agreement-check` 协议审查、`cap-table` 股权结构设计、`startup-legal` 创业法务一条龙
- **3 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：lhg-sl-contracts, lhg-sl-equity, lhg-sl-setup
- **2 个专家 agent**：agreement-checker, setup-advisor
- **1 个 hooks**（`hooks/`：pre_legal_gate.py），关键操作前自动把关

## 为什么是它

不是一个 prompt，而是一套互相兜底的机制：

1. **硬门，不是提醒**：hooks 在关键操作前自动拦截或警告（见 `hooks/`），而不是只在文档里写一句"请注意"。
2. **方法论沉淀在 skill 里**：流程、检查清单、口径都写在 `skills/` 的方法论里，命令只是入口；换个 agent 平台也能复用同一套做法。
3. **可验，不是可信**：`fixtures/` 备有坏/好对照用例，`smoke_test.py` 一键验证，规则有没有生效、自己跑一遍就知道。

## 快速上手

```bash
# 1. 安装（Claude Code 里运行）
/plugin marketplace add lhg-plugs/lhg-startup-legal
/plugin install lhg-startup-legal@lhg-plugs

# 2. 创业法务一条龙：公司类型选择 → 注册流程清单 → 股权结构设计 → 核心协议清
/lhg-startup-legal:startup-legal "三个人合伙做 SaaS"
```

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-startup-legal:agreement-check` | 协议审查：逐条过关键条款检查点（争议解决/保密期限/竞业范围/违约责任）→ 占位符提醒 → 缺失条款清单（附非律师意见声… | `/lhg-startup-legal:agreement-check ./股东协议.md 股东协议` |
| `/lhg-startup-legal:cap-table` | 股权结构设计：出资/人力/资源三维打分 → 初始分配建议 → cap-table.json 校验（加总100%）→ 僵局… | `/lhg-startup-legal:cap-table "张三出资30万全职，李四技术入股"` |
| `/lhg-startup-legal:startup-legal` | 创业法务一条龙：公司类型选择 → 注册流程清单 → 股权结构设计 → 核心协议清单（附非律师意见声明）。 | `/lhg-startup-legal:startup-legal "三个人合伙做 SaaS"` |

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用：**

- 你需要协议审查时 → 用 `/lhg-startup-legal:agreement-check`
- 你需要股权结构设计时 → 用 `/lhg-startup-legal:cap-table`
- 你需要创业法务一条龙时 → 用 `/lhg-startup-legal:startup-legal`

**什么时候不用：**

- 你只需要其中一个零散能力时 → 本插件是成套流程，单点需求用更轻量的 skill 更合适
- 你希望 AI 完全自由发挥、不接受任何自查与硬门时 → 它的规则审计与 hooks 会介入（可关，但那就别装它）
- ⚠️ 声明（首屏置顶）：本插件是创业法务助手（非"专家"，弱化执业暗示），非律师意见、仅供参考；公司注册、税务、社保等政策地域差异大，内容仅供参考，重要事项请咨询执业律师。
- 你的场景不在上面命令表覆盖范围内时 → 先看命令表，没有对应命令就别硬套

## 目录结构

```
lhg-startup-legal/
├── smoke_test.py          # 一键冒烟测试
├── ATTRIBUTION.md         # 灵感来源与许可声明
├── LICENSE                # MIT
├── README.md              # 本文件
├── .claude-plugin/
├── agents/
├── commands/
├── fixtures/
├── hooks/
├── scripts/
├── skills/
```

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（本次实测 48 项全部通过）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-startup-legal/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

同门插件见 [lhg-plugs](https://github.com/lhg-plugs)，86 个插件的完整矩阵在 [marketplace](https://github.com/lhg-plugs/marketplace) 维护。

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 抖音：搜「刘老师讲AI实战」
- 微信：lhgsmsw
