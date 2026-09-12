# Image2 安装与配置

这是一个本地 Codex Skill 压缩包，内含 `image2/SKILL.md`、界面元数据、执行脚本和空白配置模板。包中没有原作者的 API Key、实际配置或生成图片。

## 安装

本包已在 macOS、Codex CLI 0.146.1 中验证。将压缩包解压，把完整的 `image2` 文件夹放入 `~/.codex/skills/`，最终应存在：

```text
~/.codex/skills/image2/SKILL.md
~/.codex/skills/image2/agents/openai.yaml
~/.codex/skills/image2/scripts/generate_from_project_config.py
~/.codex/skills/image2/image-gen-env.example.txt
```

如目标位置已存在 `image2`，请先保留该目录，特别是自己的 `image-gen-env.txt`，不要直接覆盖。当前这台电脑已安装此 Skill，无需重复安装。

也可以把 ZIP 附加给 Codex，输入：“请将这个压缩包中的 image2 Skill 安装到我的个人 Skill 目录，保留已有配置，并告诉我如何填写配置。”

Codex 通常会自动发现新增 Skill，下一轮对话可通过 `$image2` 显式调用；若尚未显示，重启 Codex 后检查。

当前官方文档将 `~/.agents/skills/` 列为个人 Skill 发现目录，并支持符号链接。本包保留现有 `~/.codex/skills/image2` 执行路径；若其他版本未识别这个目录，可在 `~/.agents/skills/` 中创建指向它的 `image2` 符号链接。已有同名目录或链接时先检查，不要覆盖。

## 填写配置

将 `image-gen-env.example.txt` 复制为同目录的 `image-gen-env.txt`，用文本编辑器填写：

- `base_url`：服务商提供的图像 API 地址。
- `api_key`：你自己的 API Key。
- `image-model`：图像模型，模板默认 `gpt-image-2.5-flare`。
- `out-path`：输出目录。模板的 `output/imagegen` 相对于调用时的工作目录；绝对路径则始终保存到指定位置。

保存后下次调用立即生效。所有项目共用 Skill 内的配置。分享此压缩包或 Skill 目录时，不要附带填写了密钥的实际配置文件。

## 运行依赖

需要 Python 3.10 或更新版本、`openai` Python 包，以及当前 Codex 环境提供的 `imagegen` 系统 Skill。执行脚本使用：

```text
${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/image_gen.py
```

该系统脚本不包含在本压缩包中。如果目标电脑缺少此文件，需要先准备对应的 `imagegen` 运行环境；仅安装本包不能补齐它。

建议将 Python 依赖安装在专用虚拟环境。以下命令适用于 macOS，使用前确认 `.venv` 为本 Skill 专用环境：

```bash
python3 -m venv "$HOME/.codex/skills/image2/.venv"
"$HOME/.codex/skills/image2/.venv/bin/python" -m pip install openai
```

调用时让 Codex 使用该环境中的 Python。不要使用 `--break-system-packages` 修改受保护的系统 Python。

## 检查与使用

填写配置后，可先在需要保存图片的项目目录执行：

```bash
"$HOME/.codex/skills/image2/.venv/bin/python" \
  "$HOME/.codex/skills/image2/scripts/generate_from_project_config.py" \
  --prompt '配置检查' --dry-run
```

干运行只显示配置位置、端点、模型、尺寸、质量和输出路径，不发送 API 请求，也不输出 API Key。它不验证余额、模型权限或网络连通性。

在 Codex 中的调用示例：

```text
$image2 生成一只戴宇航员头盔的橘猫，写实风格，方形构图
```

参考：[OpenAI 官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills)。
