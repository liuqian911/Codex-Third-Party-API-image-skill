# Codex Image2 Skill · 自定义 API 图像生成

Image2 是一个支持自定义 OpenAI 兼容图像 API 的 **Codex 生图 Skill**。通过 `$image2` 显式调用，将文字描述转换为图片；可接入第三方图像 API，并自行配置 API 地址、密钥、图像模型和输出目录。

Image2 is a **Codex image generation skill** for text-to-image workflows with custom OpenAI-compatible APIs. Invoke `$image2` explicitly to generate an image using your configured API endpoint, API key, image model, and output directory. It supports third-party image API providers that work with the bundled image generation CLI; model availability depends on your provider.

- **显式调用 / Explicit invocation**：使用 `$image2` 启用，普通生图请求不会自动触发。
- **自主配置 / Custom API configuration**：配置保存在 Skill 目录，所有项目共用；修改后下一次调用生效。
- **输出管理 / Output management**：支持相对或绝对输出路径，同名图片自动使用版本化文件名。
- **配置检查 / Dry-run validation**：使用 `--dry-run` 检查拟用配置和输出路径，不发送生图请求。

当前 Python 包装脚本支持文生图，默认每次生成一张 `1024x1024`、`high` 质量的图片。模板模型为 `gpt-image-2`，可更换为端点和系统 CLI 支持的模型。图片编辑、蒙版和批量请求尚未封装到本脚本中。虽然 `SKILL.md` 的描述包含编辑场景，但不能据此认为包装脚本支持编辑参数。

The current helper generates one image per run, with `1024x1024` size and `high` quality by default. Image editing, masks, and batch generation are not implemented in this helper. Python, the `openai` package, and Codex's system image generation CLI are required. Windows compatibility has not been fully validated; see the platform notes below.

## 安装

可以把下面这段话发送给 Codex：

```text
请从 https://github.com/liuqian911/Codex-Third-Party-API-image2-skill 仓库的 image2 目录安装 Image2 Skill。
保留已有的个人配置，如果已经安装，请先检查现状，不要直接覆盖。
安装后检查 Python、openai 包和系统 imagegen 脚本，并告诉我如何填写配置。
```

也可以从 [Releases](https://github.com/liuqian911/Codex-Third-Party-API-image2-skill/releases) 下载 `image2-skill.zip`，将其中的 `image2` 文件夹解压到个人 Skill 目录。默认执行路径为：

```text
~/.codex/skills/image2/SKILL.md
```

如果设置了 `CODEX_HOME`，对应路径为 `$CODEX_HOME/skills/image2/`。不同 Codex 版本的发现目录可能不同，详见 [安装说明](image2/INSTALL.md)。安装后若没有显示，可重新打开任务或重启 Codex。

## 运行依赖

- Python 3.10 或更新版本。
- 执行包装脚本的 Python 环境中已安装 `openai` 包。
- 当前 Codex 环境中存在系统生图脚本：`${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/image_gen.py`。
- 可用的图像 API 地址、密钥及模型权限。

系统生图脚本没有随本仓库分发。仅下载 Image2 或安装 `openai` 包，不会自动补齐该脚本。

macOS 下可在 Skill 安装完成后创建专用 Python 环境：

```bash
image2_dir="${CODEX_HOME:-$HOME/.codex}/skills/image2"
python3 -m venv "$image2_dir/.venv"
"$image2_dir/.venv/bin/python" -m pip install openai
```

调用时请让 Codex 使用这个环境的 Python。脚本不会自动搜索或激活虚拟环境。

## 用户自主配置

将 `image2/image-gen-env.example.txt` 复制为同目录的 `image-gen-env.txt`，然后用纯文本编辑器填写：

```text
base_url = https://your-provider.example/v1
api_key = REPLACE_WITH_YOUR_OWN_KEY
image-model = gpt-image-2
out-path = output/imagegen
```

示例域名和密钥占位值不可用于实际请求。`image-model` 应填写服务支持的模型名称，Skill 名称不会锁定模型。

| 字段 | 含义 |
| --- | --- |
| `base_url` | 图像 API 基础地址，应与密钥来源对应。 |
| `api_key` | 用户自己的 API Key，只放在实际配置文件中。 |
| `image-model` | 服务支持的图像模型名称。 |
| `out-path` | 图片保存目录；相对路径以运行脚本时的工作目录为基准，绝对路径固定。 |

保存后下一次调用会读取新值，无需重新安装。项目中的同名配置文件不会被读取。

配置文件须使用 **UTF-8 无 BOM** 编码。支持空行、整行 `#` 注释和带引号的值；不支持行尾注释，也不会展开 `%USERPROFILE%`、`$env:USERPROFILE` 等环境变量。重复字段以最后一次出现的值为准。

## 使用

在 Codex 中显式调用：

```text
$image2 生成一只戴宇航员头盔的橘猫，写实风格，方形构图，柔和光线，无文字和水印。
```

普通生图请求不会自动启用此 Skill，`agents/openai.yaml` 中设置了 `allow_implicit_invocation: false`。

配置完成后可先进行干运行。以下为 macOS 命令：

```bash
image2_dir="${CODEX_HOME:-$HOME/.codex}/skills/image2"
"$image2_dir/.venv/bin/python" \
  "$image2_dir/scripts/generate_from_project_config.py" \
  --prompt '配置检查' --dry-run
```

干运行会显示配置位置、端点、模型、尺寸、质量和拟用输出路径，不发送 API 请求，也不显示 API Key。它不验证密钥、网络、额度或服务端参数支持情况。

首次向外部端点发送密钥前，Skill 会要求明确确认；同一任务已经授权该端点时无需重复确认。

## 参数

| 参数 | 默认值或作用 |
| --- | --- |
| `--prompt` | 必填，生成提示词。 |
| `--size` | `1024x1024`，是否支持由系统 CLI 和服务端决定。 |
| `--quality` | `high`。 |
| `--out` | 默认 `image2-output.png`；相对路径放在 `out-path` 下，绝对路径直接作为输出目标。 |
| `--force` | 允许覆盖指定输出文件。 |
| `--dry-run` | 只检查配置和拟用路径。 |
| `--help` | 显示帮助。 |

同名文件存在时，默认尝试 `-v2` 至 `-v999` 的可用名称。当前没有并发文件名锁。脚本不提供 `--image`、`--mask`、`--n`、`--config`、`--model` 或格式转换参数。

## 平台兼容性

已完成的安装识别验证环境为 macOS、Codex CLI 0.146.1。Python 核心使用跨平台接口，但当前版本不能视为 Windows 开箱即用版本：

- `SKILL.md` 和随包安装说明中的执行命令采用 Bash 语法，不能直接复制到 PowerShell。
- Windows 虚拟环境使用 `.venv\Scripts\python.exe`，需要在目标电脑重新创建环境与安装依赖。
- 目标环境必须能在脚本指定的位置找到系统 `image_gen.py`。
- 当前配置解析不兼容 UTF-8 BOM 或 UTF-16；模板若用这些编码保存会报错。
- 尚未在 Windows 真机上完成实际生图验证。

WSL2 中需使用 Linux 的 Python 环境和路径。Windows 原生环境与 WSL 的环境、目录不能混用。请依据 [官方 Windows 说明](https://learn.chatgpt.com/docs/windows/windows-app)核对目标环境。

## 文件结构

```text
image2/
  SKILL.md
  INSTALL.md
  image-gen-env.example.txt
  agents/openai.yaml
  scripts/generate_from_project_config.py
```

包装脚本文件名沿用旧名称，但配置现在固定读取自 Skill 根目录。它将端点和密钥通过子进程环境变量传递给系统 CLI，提示词、模型和输出参数通过参数列表传递。

## 常见问题

- **找不到配置**：从模板创建 Skill 根目录中的 `image-gen-env.txt`，填写全部四个字段。
- **找不到系统 CLI**：核对 Codex 的系统 imagegen 安装状态；本包没有包含它。
- **缺少 openai 包**：在实际执行脚本的 Python 环境中安装，另一个 Python 环境中的安装不会生效。
- **429 或 503**：根据完整错误和所配服务的状态判断原因。第三方端点报错不能直接等同于 OpenAI 官方限流。
- **图片尺寸与请求不一致**：打开实际文件查看像素尺寸，并根据端点的返回结果验收。

## 配置保护与更新

不要提交或分享实际 `image-gen-env.txt`、API Key、`.venv` 或生成图片。本仓库提供了 `.gitignore`，发布 ZIP 也仅包含五个分发文件。密钥不会因为放在本地文本文件中而被加密。

更新前备份自己的配置。当前 GitHub 首发保留原打包版 Skill 代码，仅增加仓库说明和忽略规则；Windows 适配及编辑、批处理能力需在后续版本中单独实现和验证。

参考：[OpenAI 官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills)。
