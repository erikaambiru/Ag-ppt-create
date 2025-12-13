# Archive Scripts

このフォルダには、非推奨になったスクリプトや一回限りのスクリプトを保存しています。

## 非推奨スクリプト（deprecated）

| スクリプト                                | 用途                | 非推奨理由               |
| ----------------------------------------- | ------------------- | ------------------------ |
| `convert_html.js.deprecated`              | HTML → PPTX 変換    | template 方式に置き換え  |
| `convert_html_cli.js.deprecated`          | HTML → PPTX CLI     | template 方式に置き換え  |
| `convert_html_multi.js.deprecated`        | 複数 HTML 一括変換  | template 方式に置き換え  |
| `convert_html.instructions.md.deprecated` | HTML 変換手順書     | template 方式に置き換え  |
| `extract_main_slides.py.deprecated`       | スライド間引き      | summarize 方式に置き換え |
| `router.agent.md.deprecated`              | Router エージェント | classify_input.py に統合 |
| `create_pptx_from_json.js.deprecated`     | JSON → PPTX         | create_pptx.js に統合    |

## ユーティリティスクリプト

| スクリプト               | 用途                     | 備考       |
| ------------------------ | ------------------------ | ---------- |
| `gen_sample_template.js` | テスト用テンプレート生成 | 開発用     |
| `analyze_pptx.py`        | PPTX 内容分析            | デバッグ用 |

## イベント・記事用スクリプト

| スクリプト                           | 用途                                    | 作成日  |
| ------------------------------------ | --------------------------------------- | ------- |
| `create_avd_ignite2025_pptxgenjs.js` | AVD Ignite 2025 イベント向け PPTX 生成  | 2025/12 |
| `create_codespaces_jupyter_pptx.py`  | Codespaces Jupyter 記事向け PPTX 生成   | 2025/12 |
| `generate_vnet_tap_pptx.js`          | VNet TAP 記事向け PPTX 生成             | 2025/12 |
| `create_ja_summary_com.ps1`          | BRK252 日本語サマリー生成（COM 自動化） | 2025/12 |

## 注意

- これらのスクリプトはメインのワークフローでは使用されません
- 参考実装として保存されています
- 新規スクリプト作成時のサンプルとして活用できます
