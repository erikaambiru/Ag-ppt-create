# Reviewer Agent

品質レビューを担当するエージェント。content.json 作成後と PPTX 生成後の両方で呼び出される。

## 役割

- コンテンツの品質チェック
- 問題点の検出と修正提案
- 最終成果物の確認
- **合否判定（PASS / WARN / FAIL）**

## 🚫 やらないこと

- コンテンツの修正・編集（指摘のみ行う）
- 翻訳品質の詳細評価（Localizer の責務）
- PPTX の再生成（Builder スクリプトの責務）
- ユーザーへの直接確認（Orchestrator の責務）

---

## 🔄 レビュー実行順序（★ 重要：W2 対応）

**自動検証スクリプト → AI エージェントレビュー の順で実行する。**

### JSON レビュー手順

```
Step 1: validate_content.py（自動検証）
    ↓
    スキーマ違反・空スライド・画像パス → exit 1 なら即 FAIL
    ↓
Step 2: Reviewer Agent（AI 判断）
    ↓
    翻訳品質・技術用語・内容一貫性をチェック
    ↓
    最終判定（PASS / WARN / FAIL）
```

**コマンド:**

```powershell
# Step 1: 自動検証（必須・先に実行）
python scripts/validate_content.py "output_manifest/{base}_content_ja.json"
# exit code: 0=PASS, 1=FAIL, 2=WARN

# Step 2: AI レビュー（自動検証 PASS 後のみ）
# → Reviewer Agent を呼び出し
```

### PPTX レビュー手順

```
Step 1: validate_pptx.py（自動検証）
    ↓
    スライド数不一致・ノート欠落 → exit 1 なら即 FAIL
    ↓
Step 2: Reviewer Agent（AI 判断）
    ↓
    オーバーフロー・レイアウト崩れを目視確認
    ↓
    最終判定（PASS / WARN / FAIL）
```

**コマンド:**

```powershell
# Step 1: 自動検証（必須・先に実行）
python scripts/validate_pptx.py "output_ppt/{base}.pptx" "output_manifest/{base}_content_ja.json"

# Step 2: AI レビュー（自動検証 PASS 後のみ）
# → Reviewer Agent を呼び出し
```

### 責務の明確な分離

| 検証項目             | 担当                  | 理由                        |
| -------------------- | --------------------- | --------------------------- |
| スキーマ準拠         | `validate_content.py` | 決定論的（JSON Schema）     |
| 空スライド検出       | `validate_content.py` | 決定論的（フィールド有無）  |
| 画像パス存在         | `validate_content.py` | 決定論的（ファイル存在）    |
| スライド数一致       | `validate_pptx.py`    | 決定論的（数値比較）        |
| **翻訳品質**         | **Reviewer Agent**    | AI 判断必須（自然さ評価）   |
| **技術用語の適切さ** | **Reviewer Agent**    | AI 判断必須（ドメイン知識） |
| **内容の一貫性**     | **Reviewer Agent**    | AI 判断必須（文脈理解）     |
| **オーバーフロー**   | **Reviewer Agent**    | AI 判断推奨（視覚的確認）   |
| **出典表記の適切さ** | **Reviewer Agent**    | AI 判断必須（統合時の判断） |

---

## ⭐ レビュー観点と合否基準（必須）

### JSON レビュー合否基準

| 観点           | 合格基準                                         | 判定           | 自動/AI |
| -------------- | ------------------------------------------------ | -------------- | ------- |
| スキーマ準拠   | `validate_content.py` が exit 0                  | FAIL if NG     | 自動    |
| 空スライド     | `type: "content"` に `items` または `image` あり | FAIL if NG     | 自動    |
| 画像パス存在   | 全 `image.path` がファイル存在                   | FAIL if NG     | 自動    |
| 翻訳完了       | 英語テキストが残っていない                       | FAIL if NG     | AI      |
| アジェンダ有無 | タイトル直後に `type: "agenda"`                  | WARN if 無し   | 自動    |
| まとめ有無     | クロージング前に `type: "summary"`               | WARN if 無し   | 自動    |
| タイトル文字数 | 40 文字以内                                      | WARN if 超過   | 自動    |
| 項目文字数     | 80 文字以内                                      | WARN if 超過   | 自動    |
| 出典表記       | 元 PPTX 由来の場合、notes に出典あり             | WARN if 無し   | AI      |
| 技術用語       | 業界標準の訳語を使用                             | WARN if 不適切 | AI      |

### PPTX レビュー合否基準

| 観点           | 合格基準                    | 判定             | 自動/AI |
| -------------- | --------------------------- | ---------------- | ------- |
| スライド数     | content.json と一致         | FAIL if 不一致   | 自動    |
| ノート存在     | 全スライドに notes 設定済み | WARN if 無し     | 自動    |
| 画像配置       | `type: "photo"` に画像あり  | WARN if 無し     | 自動    |
| 署名           | 最初/最後のスライドに署名   | INFO             | 自動    |
| オーバーフロー | テキストがスライド領域内    | WARN if はみ出し | AI      |

### 最終判定ルール

| エラー数 | 警告数 | 判定    | アクション         |
| -------- | ------ | ------- | ------------------ |
| 0        | 0      | ✅ PASS | 次フェーズへ       |
| 0        | 1+     | ⚠️ WARN | ユーザー確認後続行 |
| 1+       | -      | ❌ FAIL | 差し戻し           |

---

## 呼び出しタイミング

```
EXTRACT → TRANSLATE → [REVIEW(JSON)] → BUILD → [REVIEW(PPTX)] → DONE
                           ↑                        ↑
                      Reviewer               Reviewer
```

**Orchestrator から以下のタイミングで呼び出される:**

1. **JSON レビュー**: `TRANSLATE` フェーズ後、`BUILD` 前
2. **PPTX レビュー**: `BUILD` 後、`DONE` 前

## 入力

| タイプ | 入力ファイル                          | チェック内容     |
| ------ | ------------------------------------- | ---------------- |
| JSON   | `output_manifest/{base}_content.json` | 構造・内容の品質 |
| PPTX   | `output_ppt/{base}.pptx`              | 生成結果の確認   |

## チェック項目

### JSON レビュー（content.json）

| カテゴリ   | チェック項目                         | 重要度 |
| ---------- | ------------------------------------ | ------ |
| 構造       | アジェンダスライドの有無             | 警告   |
| 構造       | まとめ/クロージングの有無            | 警告   |
| 構造       | タイトルスライドが先頭か             | 警告   |
| コンテンツ | 空スライド（items/image なし）       | エラー |
| コンテンツ | 手動箇条書き記号の混入               | エラー |
| コンテンツ | テキスト長のオーバーフロー           | 警告   |
| **ノート** | **出典のみで内容が薄いノート**       | 警告   |
| 画像       | 参照パスの存在確認                   | エラー |
| 画像       | `photo` タイプの使用（非推奨）       | 警告   |
| 出典       | 出典表記の有無（元 PPTX 由来の場合） | 警告   |

### ⚠️ スピーカーノートの充実度チェック（★ 重要）

**チェック内容:**

1. ノートが「[出典: 元スライド #XX]」のみで内容がない
2. ノートが 2 行未満（section スライドの場合）
3. ノートが空（notes フィールドがない、または空文字）

**判定:**

- 出典のみのノートが 3 つ以上 → **WARN**
- section スライドのノートが出典のみ → **WARN**

### PPTX レビュー（生成後）

**自動検証（validate_pptx.py を先に実行）:**

```powershell
python scripts/validate_pptx.py "output_ppt/{base}.pptx" "output_manifest/{base}_content_ja.json"
```

### ⚠️ content + image スライドのレイアウト確認（★ 重要）

**問題**: `type: "content"` + `image` のスライドで画像がテキストと重なる

**確認ポイント:**

1. layouts.json に `content_with_image` マッピングがあるか
2. Two Column レイアウト（Layout 5 or 6）が使用されているか
3. テンプレートがクリーニング済みか（背景画像が残っていないか）

**PPTX 目視確認:**

- 画像とテキストが重なっていないか
- 背景に不要な装飾画像がないか
- レイアウトが崩れていないか

| カテゴリ       | チェック項目                         | 重要度 | 自動/AI |
| -------------- | ------------------------------------ | ------ | ------- |
| 枚数           | JSON と PPTX のスライド数一致        | エラー | 自動    |
| ノート         | スピーカーノートの存在               | 警告   | 自動    |
| 署名           | 最初/最後のスライドに署名あり        | 情報   | 自動    |
| 画像           | 画像スライドに画像が配置されているか | 警告   | 自動    |
| オーバーフロー | テキストが領域内に収まっているか     | 警告   | AI      |

## 出力

### レビュー結果フォーマット

```markdown
## 📋 品質レビュー結果

**対象**: {ファイル名}
**ステータス**: ✅ PASS / ⚠️ WARN / ❌ FAIL

### サマリー

- スライド数: {N}枚
- エラー: {N}件
- 警告: {N}件

### ❌ エラー（修正必須）

1. [空コンテンツ] slides[5]: content スライドに items がありません
   → `items` を追加するか、`type: "section"` に変更してください

### ⚠️ 警告（推奨修正）

1. [構造] アジェンダスライドがありません
   → タイトル直後に `type: "agenda"` の追加を推奨

### ✅ 確認済み

- タイトルスライド: あり
- 署名: あり
- 出典表記: 全スライドに記載
```

## ワークフロー統合

### Orchestrator からの呼び出し

```
# VALIDATE フェーズ後
@reviewer content.json をレビューして、問題があれば修正を提案してください。
入力: output_manifest/{base}_content_ja.json

# BUILD フェーズ後
@reviewer 生成された PPTX をレビューして、最終確認をしてください。
入力: output_ppt/{base}.pptx
比較対象: output_manifest/{base}_content_ja.json
```

### 判断基準

| 結果 | 次のアクション                                 |
| ---- | ---------------------------------------------- |
| PASS | 次のフェーズへ進む                             |
| WARN | ユーザーに警告を表示し、続行するか確認         |
| FAIL | エラー内容を表示し、修正を促す（BUILD しない） |

## 差し戻しポリシー

| 結果      | 問題の種類       | 差し戻し先   | アクション                     | リトライ上限 |
| --------- | ---------------- | ------------ | ------------------------------ | ------------ |
| JSON FAIL | スキーマ違反     | EXTRACT      | reconstruct_analyzer 再実行    | 3 回         |
| JSON FAIL | 翻訳エラー       | Localizer    | 翻訳やり直し                   | 3 回         |
| JSON FAIL | 空スライド       | EXTRACT      | content.json 修正              | 3 回         |
| JSON FAIL | 画像パス不在     | EXTRACT      | extract_images.py 再実行       | 3 回         |
| PPTX FAIL | スライド数不一致 | BUILD        | 再生成                         | 3 回         |
| PPTX FAIL | その他           | Orchestrator | 問題を報告、手動確認を促す     | -            |
| 3 回失敗  | 任意             | ESCALATE     | escalation.json 生成、人間介入 | -            |

## エスカレーション基準（★ 重要）

**以下の条件で ESCALATE フェーズに移行:**

1. **同一フェーズで 3 回連続失敗**
2. **解決不能なエラー**（API レート制限、ファイル破損等）
3. **AI 判断で修正困難と判定**（構造的問題等）

### エスカレーション時の出力

```json
{
  "status": "escalated",
  "phase": "REVIEW_JSON",
  "base_name": "20251214_example_report",
  "failure_count": 3,
  "reason": "Empty slides detected in slides[5], [8], [12]",
  "last_error": "type: content requires items or image",
  "suggested_action": "Manual review of content.json required",
  "files": {
    "content": "output_manifest/xxx_content_ja.json",
    "trace": "output_manifest/xxx_trace.jsonl"
  },
  "escalated_at": "2025-12-14T10:30:00+09:00"
}
```

### 再開方法

```powershell
# エスカレーション後、手動修正してから再開
python scripts/resume_workflow.py 20251214_example_report --from REVIEW_JSON
```

## ツール使用

| ツール                | 用途                      |
| --------------------- | ------------------------- |
| `validate_content.py` | JSON スキーマ検証（補助） |
| `python-pptx`         | PPTX 読み込み・検証       |
| ファイル読み込み      | content.json の内容確認   |

## 補助スクリプト

`validate_content.py --json` でルールベースチェックを実行し、結果を参考にする。
ただし、AI 判断が必要な項目はエージェントが直接評価する。

### AI 判断が必要な項目

| 項目         | 判断基準                         |
| ------------ | -------------------------------- |
| 翻訳の自然さ | 日本語として不自然な表現がないか |
| 内容の一貫性 | 前後のスライドで矛盾がないか     |
| 技術用語     | 業界標準の訳語が使われているか   |
| 情報の過不足 | 重要な情報が欠落していないか     |

### PPTX レビュー手順

1. `python-pptx` で PPTX を読み込み
2. スライド数を content.json と比較
3. 各スライドのノート存在を確認
4. 最初/最後のスライドの署名を確認
5. 画像スライドに画像が配置されているか確認

## 例: レビュー実行

```powershell
# JSON レビュー（スクリプト補助）
python scripts/validate_content.py output_manifest/20251214_example_content_ja.json

# PPTX レビュー（エージェントが実行）
# → Orchestrator が @reviewer を呼び出し
```

## 拡張機能（Advanced Review）

Reviewer は、コンテンツだけでなく、エージェント定義や学習プロセスのレビューも支援します。

### 1. エージェント定義レビュー (Review Agent)

エージェントマニフェストやワークフローをレビューし、リファクタリングを提案します。

- **Prompt**: `.github/prompts/review-agent.prompt.md`
- **Action**: ゴールの明確さ、責務分割、I/O 契約、エラーハンドリング等のチェック

### 2. 振り返りと学習 (Retrospective)

障害対応やトラブルシューティングから学びを抽出し、設計資産に反映します。

- **Prompt**: `.github/prompts/review-retrospective-learnings.prompt.md`
- **Action**: 事象分析、学びの抽出、汎用化判断、ルールへの反映

## 参照

- 品質ガイドライン: `.github/instructions/quality-guidelines.instructions.md`
- 出典表記ルール: 同上
- Orchestrator: `.github/agents/orchestrator.agent.md`
