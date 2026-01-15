---
description: 如何将思源笔记与 Antigravity 联动
---

1. **获取 API 令牌**
   - 打开思源笔记。
   - 进入 `设置` -> `关于` -> `API 令牌`。
   - 复制令牌。

2. **配置环境变量**
   - 在 Antigravity 中，你可以直接告诉我你的令牌，或者手动设置环境变量 `SIYUAN_TOKEN`。

3. **测试连接**
   - 运行以下命令：
   ```bash
   # 请将 your_token 替换为实际令牌
   $env:SIYUAN_TOKEN="your_token"; python .agent/skills/siyuan/scripts/siyuan_executor.py list_notebooks
   ```

4. **开始使用**
   - 你可以问我：“帮我看看思源笔记里有哪些笔记本？”或“在思源笔记里搜索关于 AI 的内容”。
