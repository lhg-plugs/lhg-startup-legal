<!-- About 简介（推送后填写到仓库 About 栏）：
创业法务助手：公司类型选择→注册流程清单→股权结构设计→核心协议清单 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-startup-legal
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, startup-legal, company-registration, equity -->

# lhg-startup-legal：创业法务助手，从选型到协议一条龙

> ⚠️ **声明（首屏置顶）**：本插件是**创业法务助手**（非"专家"，弱化执业暗示），**非律师意见、仅供参考**；公司注册、税务、社保等政策**地域差异大**，内容仅供参考，**重要事项请咨询执业律师**。
>
> **一句话介绍**：给 AI 编程助手装上"创业法务助手"——公司类型选择 → 注册流程清单 → 股权结构设计 → 核心协议清单；**承诺性表述写入即拦截，5 条确定性规则兜底**。
>
> **一键安装**：在 Claude Code 里运行
> ```
> /plugin marketplace add lhg-plugs/lhg-startup-legal
> /plugin install lhg-startup-legal@lhg-plugs
> ```

## 它是什么

`lhg-startup-legal` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **3 个命令**（小白入口）：`startup-legal` 创业法务一条龙，`cap-table` 股权结构设计，`agreement-check` 协议审查
- **3 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：公司设立指引（四类主体对比+注册七步）、股权结构设计（三维打分+控制权校验）、核心协议清单（四类协议检查点）
- **2 个助手 agent**：创业设立顾问、协议审查员
- **1 个执业硬门 hook**：写入文件命中执业暗示/承诺性表述（保证通过/包过/律师意见等）直接拦截，"非律师意见"声明不被误拦，可一键关闭
- **5 条确定性审计规则**：纯 Python 标准库、零第三方依赖，含协议关键条款、占位符、股权加总 100%、僵局预警、非律师意见声明检查

## 合规设计：三层防护

1. **声明置顶**：README 首屏、每个 SKILL.md 开头、每条命令输出末尾，都有显著的"非律师意见"声明。
2. **写入硬门**：hook 在文件写入前扫描执业暗示/承诺性表述关键词，命中即拦截（exit 2）；`LHG_STARTUPLEGAL_ADVICE_OFF=1` 可关闭。
3. **审计兜底**：`startup_audit.py` 的 5 条规则（3 blocker + 2 warning），`agreement-check`/`cap-table` 命令逐条清零。

## 3 个命令用法

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-startup-legal:startup-legal` | 选型→注册→股权→协议一条龙 | `/lhg-startup-legal:startup-legal "三个人合伙做 SaaS"` |
| `/lhg-startup-legal:cap-table` | 股权结构设计与校验 | `/lhg-startup-legal:cap-table "张三出资30万全职，李四技术入股"` |
| `/lhg-startup-legal:agreement-check` | 协议条款完整性审查 | `/lhg-startup-legal:agreement-check ./股东协议.md 股东协议` |

## 目录结构

```
lhg-startup-legal/
├── .claude-plugin/          # plugin.json（插件清单）+ marketplace.json（本仓即市场）
├── commands/                # 3 个命令：startup-legal / cap-table / agreement-check
├── skills/                  # 3 个平台中立 skill（设立/股权/协议，声明置顶）
├── agents/                  # 2 个助手 agent（setup-advisor / agreement-checker）
├── hooks/                   # 执业暗示/承诺性表述拦截 hook（fail-open，可一键关闭）
├── scripts/audit/           # 确定性审计：startup_audit.py（零第三方依赖）
├── fixtures/                # 好/坏对照用例
├── smoke_test.py            # 冒烟测试
├── ATTRIBUTION.md           # 灵感来源声明
└── LICENSE                  # MIT
```

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用**
- 不知道注册公司还是个体户 → `startup-legal` 跑选型问卷
- 注册流程一头雾水，要材料清单 → `startup-legal` 输出七步清单
- 合伙人股份不知道怎么分 → `cap-table` 三维打分 + 僵局预警
- 协议草稿写完了，不确定缺什么条款 → `agreement-check` 逐条体检

**什么时候不用**
- 想要"这份协议签了有没有风险"的结论 → 本插件**不给**，完整性检查≠效力判断，请咨询执业律师
- 想要一份能直接签署的成品合同 → 本插件不提供，只给检查点清单
- 想要律师代理注册/诉讼 → 本插件是助手不是律所，请找执业律师
- 想编造注册地址、做阴阳合同 → **直接拒绝**，这是违法的

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（JSON 合法、skill/command/agent 完整性、5 条规则、fixtures 命中、hooks 行为）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-startup-legal/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

## 组织插件矩阵（互链）

| 插件 | 一句话 | 安装 |
|---|---|---|
| [lhg-contract](https://github.com/lhg-plugs/lhg-contract) | 合同审查助手：风险条款标红+修改建议 | `/plugin install lhg-contract@lhg-plugs` |
| [lhg-labor-rights](https://github.com/lhg-plugs/lhg-labor-rights) | 劳动维权助手：仲裁维权一条龙 | `/plugin install lhg-labor-rights@lhg-plugs` |
| [lhg-ip](https://github.com/lhg-plugs/lhg-ip) | 知产保护助手：类型判断→申请流程→维权清单 | `/plugin install lhg-ip@lhg-plugs` |
| [lhg-bp](https://github.com/lhg-plugs/lhg-bp) | 商业计划书专家：九章BP→投资人自检→路演版 | `/plugin install lhg-bp@lhg-plugs` |
| [lhg-fullstack](https://github.com/lhg-plugs/lhg-fullstack) | 小白一句话 → 高质量全栈应用 | `/plugin install lhg-fullstack@lhg-plugs` |

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 视频号：搜「刘洪光实名上网」
- 微信：lhgsmsw
