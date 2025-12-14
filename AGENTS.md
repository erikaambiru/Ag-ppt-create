# AGENTS

PPTX 自動生成エージェント定義（再設計版）。

## 設計原則

| 原則                                 | 説明                                             | 適用例                                       |
| ------------------------------------ | ------------------------------------------------ | -------------------------------------------- |
| **SSOT** (Single Source of Truth)    | 各ルールは 1 箇所のみで定義し、他は参照          | PLAN フェーズ → `plan-phase.instructions.md` |
| **Agent vs Script**                  | AI 判断が必要 → Agent、決定論的 → Script         | 翻訳 → Agent、検証 → Script                  |
| **IR (Intermediate Representation)** | エージェント間は JSON で疎結合                   | content.json が共通言語                      |
| **Fail Fast**                        | エラーは早期検出、3 回リトライ後エスカレーション | validate → build の順序                      |
| **Human in the Loop**                | 重要な決定はユーザー確認必須                     | PLAN フェーズでの承認                        |
| **Dynamic Context**                  | テンプレート/出力先の特性は動的に取得し伝播      | スライドサイズ、フォント設定等               |
| **Complete Extraction**              | ソースの全構成要素を明示的に列挙して取得         | テキスト + 画像 + コード + メタデータ        |

> 📖 設計原則の詳細は [common.instructions.md](.github/instructions/common.instructions.md) を参照。

### ドキュメント SSOT マップ

| トピック           | 定義元（SSOT）                                            | 参照元                           |
| ------------------ | --------------------------------------------------------- | -------------------------------- |
| PLAN フェーズ確認  | `.github/instructions/plan-phase.instructions.md`         | orchestrator.agent.md, AGENTS.md |
| 命名規則・箇条書き | `.github/instructions/common.instructions.md`             | 全ファイル                       |
| 品質ガイドライン   | `.github/instructions/quality-guidelines.instructions.md` | エージェント定義                 |
| ツール使用フロー   | `.github/instructions/tools-reference.instructions.md`    | AGENTS.md                        |
| IR スキーマ        | `workspace/content.schema.json`                           | スクリプト、エージェント         |

## エージェント一覧と責務

| エージェント  | マニフェスト                           | 役割                                            | 種別       |
| ------------- | -------------------------------------- | ----------------------------------------------- | ---------- |
| Orchestrator  | `.github/agents/orchestrator.agent.md` | 状態管理・計画・ヒアリング・リトライ制御        | **Agent**  |
| Localizer     | `.github/agents/localizer.agent.md`    | 翻訳のみ（AI 判断必須）                         | **Agent**  |
| Summarizer    | `.github/agents/summarizer.agent.md`   | 要約・再構成のみ（AI 判断必須）                 | **Agent**  |
| Reviewer      | `.github/agents/reviewer.agent.md`     | 品質レビュー（JSON・PPTX 両対応）               | **Agent**  |
| Classifier    | `scripts/classify_input.py`            | 入力分類・方式判定（純粋関数）                  | **Script** |
| Validator     | `scripts/validate_content.py`          | IR スキーマ検証・空コンテンツ検出・画像パス検証 | Script     |
| PPTXValidator | `scripts/validate_pptx.py`             | PPTX 検証（スライド数・ノート・画像）           | Script     |
| Builder       | `scripts/create_from_template.py`      | PPTX 生成（決定論的処理）                       | Script     |
| Tracer        | `scripts/workflow_tracer.py`           | ワークフロー観測・トレースログ出力              | Script     |

### 単一責任原則（SRP）によるエージェント分離

| エージェント | 責務カテゴリ | 責務                                 |
| ------------ | ------------ | ------------------------------------ |
| Orchestrator | 制御         | 状態管理・計画・ヒアリング・リトライ |
| Localizer    | 変換         | 翻訳のみ                             |
| Summarizer   | 変換         | 要約・再構成のみ                     |
| Reviewer     | 検証         | AI 判断が必要なレビュー              |

## スクリプト一覧

| ツール                 | 用途                                           |
| ---------------------- | ---------------------------------------------- |
| `classify_input.py`    | 入力分類・方式判定（旧 Router の純粋関数化）   |
| `workflow_tracer.py`   | 観測性・トレースログ機能                       |
| `resume_workflow.py`   | エスカレーション後の再開                       |
| `clean_template.py`    | テンプレートから背景画像・不要要素を削除       |
| `diagnose_template.py` | テンプレート品質診断（背景画像、壊れた参照等） |
| `validate_pptx.py`     | PPTX 検証（スライド数・ノート・画像）          |

## 共通 I/O 契約

- base: `{YYYYMMDD}_{keyword}_{purpose}`
- ユーザー入力: `input/` （PPTX ファイル、URL リスト、Markdown 等）※ユーザーが手動配置するもののみ
- 中間生成物: `output_manifest/` （API 取得結果、content.json、inventory.json 等すべての自動生成ファイル）
  - `{base}_classification.json` - 入力分類結果（classify_input.py 出力）
  - `{base}_article.json` - Web 記事の取得結果
  - `{base}_content.json` - IR 形式のコンテンツ
  - `{base}_content_ja.json` - 翻訳済み IR
  - `{base}_trace.jsonl` - ワークフロートレースログ
  - `{base}_escalation.json` - エスカレーション状態（失敗時）
  - `{base}_inventory.json` - シェイプ一覧
  - `{base}_working.pptx` - 作業用 PPTX
  - `{template_stem}_layouts.json` - レイアウト設定（analyze_template.py 出力）
- 画像: `images/{base}/`
- 最終出力: `output_ppt/{base}.pptx`
- すべて UTF-8、JSON は schema バリデート必須。
- **スキーマ定義**:
  - IR スキーマ: `workspace/content.schema.json` (v1.0.0)
  - 分類スキーマ: `workspace/classification.schema.json` (v1.0.0)

## 標準フロー（簡素化版）

```
INIT → PLAN(確認) → PREPARE_TEMPLATE → EXTRACT → [SUMMARIZE] → TRANSLATE → REVIEW(JSON) → BUILD → REVIEW(PPTX) → DONE
          ↑                                           │                        │                      │
          │                                      (枚数削減時)                   │                      │
          │                      └─────────(FAIL→修正 最大3回)─────────────────┴──────────────────────┘
          │                                           ↓
     ユーザー承認必須                            ESCALATE(3回超)
```

### フェーズ詳細

| フェーズ             | 担当                    | 処理内容                                                 | トレース |
| -------------------- | ----------------------- | -------------------------------------------------------- | -------- |
| INIT                 | classify_input.py       | 入力検出、base 生成、方式判定 → classification.json 出力 | ✅       |
| PLAN                 | Orchestrator            | ユーザーに方式・枚数を提示し承認を得る（★ 必須）         | ✅       |
| **PREPARE_TEMPLATE** | clean_template.py       | テンプレート品質診断・クリーニング                       | ✅       |
| EXTRACT              | スクリプト群            | 画像抽出 + レイアウト分析 + content.json 生成（並列可）  | ✅       |
| **SUMMARIZE**        | **Summarizer**          | 枚数削減時のみ：要約・再構成（AI 判断）                  | ✅       |
| TRANSLATE            | Localizer               | content.json → content_ja.json（翻訳のみ）               | ✅       |
| **REVIEW(JSON)**     | **Reviewer**            | content.json の品質チェック（構造・内容）→ 合否判定      | ✅       |
| BUILD                | create_from_template.py | PPTX 生成                                                | ✅       |
| **REVIEW(PPTX)**     | **Reviewer**            | 生成された PPTX の最終確認 → 合否判定                    | ✅       |
| DONE                 | Orchestrator            | PowerPoint 起動（オプション）                            | ✅       |
| ESCALATE             | workflow_tracer.py      | 3 回失敗時の人間エスカレーション                         | ✅       |

> 📖 PREPARE_TEMPLATE の詳細手順は [tools-reference.instructions.md](.github/instructions/tools-reference.instructions.md) を参照。

### レビュー合否基準（★ 重要）

| 判定        | 条件              | アクション            |
| ----------- | ----------------- | --------------------- |
| ✅ PASS     | エラー 0、警告 0  | 次フェーズへ          |
| ⚠️ WARN     | エラー 0、警告 1+ | ユーザー確認後続行    |
| ❌ FAIL     | エラー 1+         | 差し戻し（最大 3 回） |
| 🚨 ESCALATE | 3 回連続 FAIL     | 人間介入待ち          |

- **PLAN(確認)**: ユーザーに方式・枚数・詳しさの選択肢を提示し、承認を得てから次へ進む（★ 必須）
  - **入力フォーマット**: `{枚数}{方式}` 形式（例: `2A`, `3C`）
  - **項番ルール**: A=元 PPTX 継承(PPTX 入力時のみ), B=pptxgenjs, C=create_ja_pptx, D〜=テンプレート
  - **デフォルト**: ユーザーが未指定の場合は標準版 + 最初のテンプレート(D)を提案
- **EXTRACT**: 以下を並列実行可能
  - `analyze_template.py` → layouts.json
  - `extract_images.py` → images/
  - `reconstruct_analyzer.py` → content.json
- **ESCALATE**: 3 回失敗で Orchestrator が停止し、`{base}_escalation.json` を生成
  - 再開: `python scripts/resume_workflow.py {base} --from {phase}`

## 観測性（トレーサビリティ）

全フェーズで `workflow_tracer.py` を使用してログを記録。
トレースログは JSONL 形式で `output_manifest/{base}_trace.jsonl` に保存される。

> 📖 詳細フロー・コマンド例は [tools-reference.instructions.md](.github/instructions/tools-reference.instructions.md) を参照。

## 方式選定

| 用途                  | 推奨方式                                              | 推奨度     | 備考                 |
| --------------------- | ----------------------------------------------------- | ---------- | -------------------- |
| **英語 PPTX→ 日本語** | `reconstruct_analyzer.py` + `create_from_template.py` | ⭐⭐⭐⭐⭐ | 最推奨、マスター継承 |
| **テンプレート利用**  | `analyze_template.py` + `create_from_template.py`     | ⭐⭐⭐⭐⭐ | 最推奨、デザイン継承 |
| 白紙から新規作成      | `create_ja_pptx.py`                                   | ⭐⭐⭐⭐   | シンプルできれい     |
| コード/技術内容多     | カスタム JS (pptxgenjs)                               | ⭐⭐⭐⭐   | コードブロック向け   |

### 方式ステータス

| 方式     | 状態                           | 理由                                             |
| -------- | ------------------------------ | ------------------------------------------------ |
| preserve | **experimental（精度改善中）** | 図・グラフで崩れやすい → 現在は reconstruct 推奨 |

## 運用ルール

- `.github/copilot-instructions.md` と `.github/instructions/*.md` に従う
- すべてのツール呼び出しは I/O スキーマ整合性を確認してから実行
- テンプレート/PPTX の直接編集は禁止
- **新規テンプレート使用時は `analyze_template.py` でレイアウト設定を生成**

---

## トラブルシューティング

過去の問題と対策は **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** を参照。

> 💡 各問題はスクリプト改修により自動対処されています。新しい問題が発生したら TROUBLESHOOTING.md に追記してください。
