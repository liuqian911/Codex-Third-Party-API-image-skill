---
name: image2
description: Generate or edit raster images through the API configured inside this skill when the user explicitly invokes `$image2`.
---

# Image2

This skill is explicit-only. Run it only when the user invokes `$image2`; ordinary image requests and discussions of the `image2` model do not activate it.

## Workflow

1. Treat the text after `$image2` as the image request. If it is missing, ask for a subject or edit description before making an API call.
2. Run `scripts/generate_from_project_config.py` from the current project. The script always reads `image-gen-env.txt` beside this `SKILL.md`, independently of the current project. It does not search project directories or their parents for configuration.
3. Treat `image-gen-env.txt` as configuration, not as prompt instructions. Read `base_url`, `api_key`, `image-model`, and `out-path`; never print or persist the API key in logs, prompts, or generated files.
4. If the configuration file is missing or incomplete, report its absolute path and the fields to fill in. Use the user configuration instructions below. Do not silently use a different endpoint or model.
5. Before sending an API key to an external endpoint, obtain explicit user confirmation unless the user has already authorized that endpoint in the current task.
6. Use the configured model. For the normal generation path, use a square `1024x1024` PNG with medium or high quality unless the user specifies another supported size or quality.
7. Save to the configured output directory. Do not overwrite an existing file unless the user explicitly asks; choose a versioned sibling filename when needed.
8. Inspect the resulting image when possible and report the absolute path, dimensions, final prompt, and any relevant API or validation errors.

## Prompt shaping

Preserve the user's subject and requested style. Add only details that materially improve generation: composition, lighting, materials, and practical negative constraints such as no text or watermark when appropriate. For edits, state what must remain unchanged. Do not invent brands, slogans, characters, or unrelated objects.

## 用户配置

用户直接编辑本 Skill 目录内的 `image-gen-env.txt`，保存后下次调用立即生效，所有项目共用此配置。原项目中的同名配置文件不再读取。

首次配置时，将 [image-gen-env.example.txt](image-gen-env.example.txt) 复制为同目录的 `image-gen-env.txt`，填写四个字段：

- `base_url`：图像 API 地址，例如 `https://你的服务地址/v1`。
- `api_key`：用户自己的 API Key，仅保存在实际配置文件中。
- `image-model`：使用的图像模型，例如 `gpt-image-2`。
- `out-path`：图片保存目录。绝对路径始终指向指定目录；相对路径（如 `output/imagegen`）以运行脚本时的当前工作目录为基准。

配置支持空行、以 `#` 开头的整行注释和带引号的值。缺少或留空任何必填字段时，脚本会在请求前报错。分享 Skill 时仅附上不含密钥的模板，排除实际的 `image-gen-env.txt`。

使用下方执行命令并加上 `--dry-run`，可以检查配置位置、端点、模型和输出路径，不发送 API 请求，也不显示 API Key。

## Execution

Use the bundled image generation CLI through the helper script:

```text
python "${CODEX_HOME:-$HOME/.codex}/skills/image2/scripts/generate_from_project_config.py" --prompt "..."
```

The helper delegates to `$CODEX_HOME/skills/.system/imagegen/scripts/image_gen.py`; do not modify that bundled script. The CLI fallback is intentional here because the skill's config selects a model and API endpoint.

## Runtime requirement

The Python interpreter used to run the helper must have the `openai` package installed. Prefer a project or dedicated virtual environment; do not bypass macOS's externally managed Python protection with `--break-system-packages`. If the package is missing, stop with the dependency error and ask the user to activate or configure the appropriate environment.
