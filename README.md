# voice-claude

语音驱动的 Claude 副屏助手（开发中）。

**目标**：按住全局热键说话 → 本地语音识别转文字 → 发送给 Claude Code 执行 → 答案流式显示在置顶半透明副屏里，全程不用来回切换窗口。

## 进度

- [x] 第一步：按住左Alt录音，松开保存为 wav（recorder.py）
- [ ] 第二步：faster-whisper 语音转文字
- [ ] 第三步：接入 Claude Agent SDK，让语音指令驱动 Claude Code
- [ ] 第四步：半透明置顶副屏窗口（Flet）
- [ ] 第五步：打包成 skill 分享给别人

## 技术栈

- Python 3.13
- sounddevice（录音）、pynput（全局热键）、wave（wav 保存）
- faster-whisper（本地语音识别，计划）
- claude-agent-sdk（与 Claude Code 通信，计划）
- Flet（副屏窗口，计划）

## 使用

```bash
pip install sounddevice pynput faster-whisper
python recorder.py   # 按住左Alt说话，松开保存 test.wav，Esc 退出
```
