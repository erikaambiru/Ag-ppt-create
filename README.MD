# Ag-ppt-create

> 🤖 AI エージェントが PowerPoint を自動生成するためのツールキット

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18+-339933?logo=node.js&logoColor=white)](https://nodejs.org)

[python-pptx](https://python-pptx.readthedocs.io/) と [PptxGenJS](https://gitbrent.github.io/PptxGenJS/) を使用した PPTX 自動生成ツールキットです。

---

## 🚀 クイックスタート

### 1. セットアップ（初回のみ）

```powershell
git clone https://github.com/aktsmm/Ag-ppt-create.git
cd Ag-ppt-create

# Python 環境
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Node.js 環境
npm install
```

👉 **[詳細なセットアップ手順](docs/SETUP.md)**

### 2. テンプレートを準備

`templates/` フォルダに**普段使っている PowerPoint テンプレート**を入れてください。

```powershell
# 例：自社テンプレートをコピー
Copy-Item "C:\Users\あなた\Documents\会社テンプレート.pptx" "templates/"
```

> 💡 **ポイント**: よく使う PowerPoint をテンプレートとして入れておくと、そのデザイン（配色・フォント・レイアウト）を継承した PPTX が生成されます。
>
> 📖 **しっかり作りたい場合**: スライドマスターやプレースホルダーの設計については **[テンプレート設計ガイド](docs/TEMPLATE-DESIGN.md)** を参照してください。

### 3. 使う

VS Code で GitHub Copilot の **Agent モード** → **Orchestrator** を選択して話しかけるだけ。

```
この記事から PowerPoint 作って
https://example.com/article

このPPTXを日本語化して
[英語版PPTX を input/ に配置]
```

> ⚠️ **PPTX ファイルの入力**: VS Code のチャットには PPTX をドラッグ＆ドロップできません。`input/` フォルダにファイルを配置してください。

Orchestrator が方式・枚数を提案し、**あなたの承認後**に生成を開始します。

---

## 📥 対応する入力

| 入力タイプ   | 例                                            |
| ------------ | --------------------------------------------- |
| **URL**      | ブログ記事、ドキュメント、Qiita、Zenn 等      |
| **PPTX**     | 英語版 PowerPoint（日本語化）                 |
| **テキスト** | 箇条書きメモ、議事録、要件定義                |
| **画像**     | スクリーンショット、手書きメモ、図解          |
| **ファイル** | Markdown、Word、PDF（テキスト抽出可能なもの） |

---

## ⚖️ ライセンスと使用条件

本プロジェクトは **CC BY-NC-SA 4.0** ライセンスの下で提供されています。
詳細は [LICENSE](LICENSE) をご確認ください。

## 機能

### 主要スクリプト

| スクリプト                | 用途                                    |
| ------------------------- | --------------------------------------- |
| `classify_input.py`       | ★ 入力分類・方式判定（純粋関数）        |
| `reconstruct_analyzer.py` | ★ 英語版 PPTX → content.json 抽出       |
| `create_from_template.py` | ★ テンプレート継承で PPTX 生成          |
| `validate_content.py`     | ★ IR スキーマ検証・空コンテンツ検出     |
| `validate_pptx.py`        | ★ PPTX 検証（スライド数・ノート・画像） |
| `workflow_tracer.py`      | ★ ワークフロー観測・トレースログ        |
| `resume_workflow.py`      | ★ エスカレーション後の再開              |
| `analyze_template.py`     | テンプレートのレイアウト分析            |
| `diagnose_template.py`    | テンプレート品質診断                    |
| `clean_template.py`       | テンプレートから不要要素を削除          |
| `extract_images.py`       | PPTX から画像を抽出                     |
| `extract_parallel.ps1`    | EXTRACT フェーズの並列実行              |
| `create_ja_pptx.py`       | 白紙から新規 PPTX 作成                  |
| `create_pptx.js`          | pptxgenjs で PPTX 作成                  |
| `pptx-signature.js`       | PPTX 署名追加ヘルパー                   |
| `summarize_content.py`    | 全体把握 → 要約再構成（AI 連携）        |

### 補助スクリプト

| スクリプト          | 用途                        |
| ------------------- | --------------------------- |
| `reorder_slides.py` | スライドの並び替え・複製    |
| `extract_shapes.py` | テキスト構造を JSON 抽出    |
| `apply_content.py`  | テンプレート内テキスト置換  |
| `check_overflow.py` | bbox 事前検証               |
| `gen_preview.py`    | PPTX からサムネイル画像生成 |

> 💡 **画像埋め込み対応**: `create_from_template.py`、`create_ja_pptx.py`、`create_pptx.js` は content.json 内の `image` フィールドで画像埋め込みに対応しています。

## ⚠️ セキュリティ

本プロジェクトは外部モジュールに依存しています。サプライチェーンリスクや脆弱性報告については **[SECURITY.md](.github/SECURITY.md)** を参照してください。

---

## エージェントワークフロー

本リポジトリは **3 つのエージェント** と **決定論的スクリプト群** がチームで PPTX を生成します。

### 前提条件

- **VS Code** + **GitHub Copilot 拡張機能**
- **Agent モード対応モデル**が必須（Agent モード非対応のモデルでは動作しません）

### モデル要件（重要）

- **前提**: 本リポジトリのエージェントワークフローは、エージェントワークフローに対応した AI モデルが必要です。非対応モデルでは、レビュー・差し戻しループが動作しません。
- **推奨モデル**: Claude Opus 4（エージェントワークフロー互換。レビュー反復の安定性が高い）
- **動作保証の範囲**: 上記モデルでの動作を前提に品質ゲート・チェックポイント設計を行っています。

### エージェント構成（再設計版）

| エージェント     | 役割                                     | 種別   |
| ---------------- | ---------------------------------------- | ------ |
| **Orchestrator** | 状態管理・計画・ヒアリング・リトライ制御 | Agent  |
| **Localizer**    | 翻訳のみ（AI 判断必須）                  | Agent  |
| **Summarizer**   | 要約・再構成（AI 判断必須）              | Agent  |
| **Reviewer**     | 品質レビュー（JSON・PPTX 両対応）        | Agent  |
| Classifier       | 入力分類・方式判定                       | Script |
| Validator        | IR スキーマ検証・空コンテンツ検出        | Script |
| PPTXValidator    | PPTX 検証（スライド数・ノート・画像）    | Script |
| Builder          | PPTX 生成（決定論的処理）                | Script |
| Tracer           | ワークフロー観測・トレースログ出力       | Script |

### 4 つの生成方式

| 方式            | 説明                                  | 使用ツール                                            | 推奨度            |
| --------------- | ------------------------------------- | ----------------------------------------------------- | ----------------- |
| **template** ⭐ | テンプレート継承で任意枚数生成        | `analyze_template.py` + `create_from_template.py`     | ⭐⭐⭐⭐⭐ 最推奨 |
| **python-pptx** | JSON からシンプルできれいに新規作成   | `create_ja_pptx.py`                                   | ⭐⭐⭐⭐ オススメ |
| **pptxgenjs**   | JS スクリプトで直接生成（コード向け） | カスタム JS                                           | ⭐⭐⭐⭐ オススメ |
| **reconstruct** | 英語 PPTX → 日本語化（マスター継承）  | `reconstruct_analyzer.py` + `create_from_template.py` | ⭐⭐⭐⭐⭐ 最推奨 |

> 💡 Orchestrator が入力タイプに応じて最適な方式を自動提案します。
> 英語版 PPTX の場合は **reconstruct 方式**、Web 記事の場合は **template 方式**が選択されます。

## 方式選択ガイド

### 選択フローチャート

```
英語版 PPTX を日本語化したい？
├─ YES → reconstruct（最推奨）⭐⭐⭐⭐⭐
│
└─ NO
    ├─ テンプレートがある？
    │   └─ YES → template（最推奨）⭐⭐⭐⭐⭐
    │
    ├─ コード/技術内容が多い？
    │   └─ YES → pptxgenjs ⭐⭐⭐⭐
    │
    └─ 一般的な内容
        └─ python-pptx ⭐⭐⭐⭐
```

### 各方式の特徴

#### template（テンプレート継承）⭐⭐⭐⭐⭐ 最推奨

- **メリット**: 企業テンプレートのデザインをそのまま継承、任意枚数生成可能
- **デメリット**: テンプレートが正しく設計されている必要あり
- **使用ツール**: `analyze_template.py` → `create_from_template.py`
- **推奨用途**: 社内標準テンプレートがある場合

#### python-pptx（白紙から新規）⭐⭐⭐⭐ オススメ

- **メリット**: シンプルできれい、依存少ない、安定性高い
- **デメリット**: デザインのカスタマイズは限定的
- **使用ツール**: `create_ja_pptx.py`
- **推奨用途**: テンプレートがない場合のデフォルト

#### pptxgenjs（JavaScript 直接）⭐⭐⭐⭐ オススメ

- **メリット**: シンプルできれい、コードブロック表示に強い
- **デメリット**: Node.js 必要
- **使用ツール**: カスタム JS スクリプト
- **推奨用途**: 技術内容・コードが多い場合

#### reconstruct（英語 PPTX 日本語化）⭐⭐⭐⭐⭐ 最推奨

- **メリット**: 元 PPTX のスライドマスターを完璧に継承、レイアウト最適化
- **デメリット**: 英語版 PPTX 入力が必要
- **使用ツール**: `reconstruct_analyzer.py` → Localizer Agent → `create_from_template.py`
- **推奨用途**: 英語版 PPTX を日本語化する場合

> ⚠️ **preserve 方式**（既存シェイプを直接編集）は experimental です。図・グラフで崩れやすいため、現在は reconstruct 方式を推奨しています。

---

### クイックチェックリスト

テンプレートを作成・選定する際の最低限の確認事項：

| 項目               | 推奨                                                       |
| ------------------ | ---------------------------------------------------------- |
| **スライドサイズ** | 16:9（13.33" × 7.5"）                                      |
| **必須レイアウト** | Title / Content / Section / Blank の 4 種類以上            |
| **プレースホルダ** | 固定テキストボックスではなく、TITLE/BODY を使用            |
| **フォント**       | Windows 標準（Segoe UI, Yu Gothic UI）推奨                 |
| **コントラスト**   | WCAG 4.5:1 以上（黒 on 白、白 on 濃色）                    |
| **レイアウト名**   | 英語キーワード含む（"Title Slide", "Section Header" など） |

### レイアウト不足時の自動補完

テンプレートに必要なレイアウト（title, content, section, two_content, blank, agenda, closing）が不足している場合、PowerPoint COM で自動生成できます：

```powershell
# レイアウト確認
.\scripts\ensure_layouts.ps1 -InputPath "templates\mytemplate.pptx"

# 不足レイアウトを自動追加
.\scripts\create_master_set.ps1 -InputPath "templates\mytemplate.pptx" -OutputPath "templates\mytemplate_complete.pptx"
```

### 本ツールキットでの使い方

```powershell
# 1. テンプレートのレイアウトを分析（初回のみ）
python scripts/analyze_template.py templates/mytemplate.pptx
# → output_manifest/mytemplate_layouts.json が生成される

# 2. PPTX 生成（レイアウト設定は自動検出）
python scripts/create_from_template.py templates/mytemplate.pptx content.json output.pptx
```

### content.json でのスライドタイプ指定

```json
{
  "slides": [
    { "type": "title", "title": "発表タイトル", "subtitle": "サブタイトル" },
    { "type": "agenda", "title": "目次", "items": ["項目1", "項目2"] },
    { "type": "content", "title": "本文", "items": ["箇条書き1", "箇条書き2"] },
    { "type": "closing", "title": "Thank You" }
  ]
}
```

`type` で指定すると `layouts.json` に従ってレイアウトが選択されます。直接指定する場合は `"layout": 9` のように番号を使用。

> 📖 スライドマスターの詳細、プレースホルダの設計、配色・フォントのベストプラクティスは **[テンプレート設計ガイド](docs/TEMPLATE-DESIGN.md)** を参照してください。

---

### ワークフロー図

```
[ユーザー入力]
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  INIT: [classify_input.py] 入力分類・方式判定               │
│    出力: {base}_classification.json                         │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  PLAN: [Orchestrator] ユーザー確認（★必須）                 │
│    方式・枚数・詳しさを提示し承認を得る                     │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  EXTRACT: [スクリプト群] 並列抽出                           │
│    analyze_template.py / extract_images.py /                │
│    reconstruct_analyzer.py → {base}_content.json            │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  TRANSLATE: [Localizer] AI 翻訳                             │
│    出力: {base}_content_ja.json                             │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  REVIEW(JSON): [Reviewer] 品質チェック → 合否判定           │
│    PASS → BUILD / FAIL → 差し戻し（最大3回）                │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  BUILD: [create_from_template.py] PPTX 生成                 │
│    出力: output_ppt/{base}.pptx                             │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  REVIEW(PPTX): [Reviewer] 最終確認 → 合否判定               │
│    PASS → DONE / FAIL → 差し戻し / 3回失敗 → ESCALATE       │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  DONE: PowerPoint 起動（オプション）                        │
│    最終出力: output_ppt/{base}.pptx                         │
└─────────────────────────────────────────────────────────────┘

※ {base} = {YYYYMMDD}_{keyword}_{purpose}
※ 3回連続失敗 → ESCALATE（人間介入待ち）
※ 再開: python scripts/resume_workflow.py {base} --from {phase}
```

詳細は [AGENTS.md](AGENTS.md) を参照。

## プロジェクト情報

### 📚 ドキュメント

- **[AGENTS.md](AGENTS.md)** — エージェント設計とワークフロー
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — 貢献ガイド
- **[ATTRIBUTION.md](ATTRIBUTION.md)** — 帰属表示ガイドライン
- **[LICENSE](LICENSE)** — ライセンス（CC BY-NC-SA 4.0）
- **[SECURITY.md](.github/SECURITY.md)** — セキュリティポリシー
- **[CODE_OF_CONDUCT.md](.github/CODE_OF_CONDUCT.md)** — 行動規範

### 🤝 Contributing

貢献を歓迎します！詳細は [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

### ⚖️ Commercial Use

商用利用をご希望の場合は、[@aktsmm](https://github.com/aktsmm) までお問い合わせください。

### 📄 Citation

本ソフトウェアを使用する場合は、以下の形式で引用してください：

```
Based on Ag-ppt-create by aktsmm
https://github.com/aktsmm/Ag-ppt-create
License: CC BY-NC-SA 4.0
```

詳細は [ATTRIBUTION.md](ATTRIBUTION.md) を参照。

## ディレクトリ構成

```
Ag-ppt-create/
├── input/             # 📥 入力ソース（PPTX、URL リスト、Markdown 等）※ユーザー手動配置
├── output_ppt/        # 📤 生成された PPTX 出力先
├── output_manifest/   # 🔧 中間生成物
│   ├── {base}_classification.json  # 入力分類結果
│   ├── {base}_content.json      # IR 形式のコンテンツ
│   ├── {base}_content_ja.json   # 翻訳済み IR
│   ├── {base}_trace.jsonl       # ワークフロートレースログ
│   └── {base}_escalation.json   # エスカレーション状態（失敗時）
├── images/            # 🖼️ 抽出・ダウンロード画像
│   └── {base}/                  # プロジェクト別画像フォルダ
├── templates/         # 📋 PPTX テンプレート
│   ├── sample.pptx              # サンプルテンプレート
│   └── template.pptx            # 汎用テンプレート
├── scripts/           # ⚙️ PPTX 操作ツール
├── workspace/         # 🗂️ スキーマ定義
│   ├── content.schema.json      # IR スキーマ (v1.0.0)
│   └── classification.schema.json  # 分類スキーマ (v1.0.0)
├── docs/              # 📚 ドキュメント
└── .github/           # 🤖 Copilot 設定・エージェント定義
    └── agents/                  # エージェント定義ファイル
```

## 参考

- [python-pptx](https://python-pptx.readthedocs.io/) - Python PPTX ライブラリ
- [PptxGenJS](https://gitbrent.github.io/PptxGenJS/) - JavaScript PPTX ライブラリ

## このリポジトリの作り方

このリポジトリは GitHub Copilot（Claude）との対話で構築しました。
すべてのスクリプトは公式ドキュメントのみを参考に独自実装しています。

👉 **[作成手順・指示例を見る](docs/HOW-I-BUILT-THIS.md)**

## コントリビュート

プルリクエスト歓迎です！詳細は [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

## ライセンス

[CC BY-NC-SA 4.0](LICENSE)（非商用・継承）
