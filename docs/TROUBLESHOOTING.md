# TROUBLESHOOTING

過去に発生した問題と対策の記録。スクリプト改修により自動対処されているものが多い。

> 📅 最終更新: 2025-12-14

---

## 目次

1. [スピーカーノートが消える](#1-スピーカーノートが消える問題)
2. [タイトルが空のスライド](#2-タイトルが空のスライドが多い問題)
3. [画像が見つからない](#3-画像が見つからない問題)
4. [GitHub Models API レート制限](#4-github-models-api-レート制限)
5. [中間ファイルが input/ に保存される](#5-中間ファイルが-input-に保存される問題)
6. [空スライドが生成される（two_column）](#6-空スライドが生成される問題two_column)
7. [画像が異常に大きく表示される](#7-画像が異常に大きく表示される問題)
8. [アイコン/ロゴが本文画像として使われる](#8-アイコンロゴが本文画像として使われる問題)
9. [position: "center" が無視される](#9-position-center-が無視される問題)
10. [翻訳後に元スライドの参照が不明](#10-翻訳後に元スライドの参照が不明になる問題)
11. [items にオブジェクト配列を使用してスキーマエラー](#11-items-にオブジェクト配列を使用してスキーマエラー)
12. [PLAN フェーズで選択肢が指定しづらい](#12-planフェーズで選択肢が指定しづらい問題)
13. [まとめスライドがあるのに警告が出る](#13-まとめスライドがあるのに警告が出る問題)
14. [背景画像がスクリーンショットに重なる](#14-背景画像がスクリーンショットに重なる問題)
15. [「この画像は表示できません」エラー](#15-この画像は表示できませんエラー)
16. [pptxgenjs でスピーカーノートが設定されない](#16-pptxgenjs-でスピーカーノートが設定されない問題)
17. [photo スライドが見にくい（タイトルと画像が離れている）](#17-photo-スライドが見にくい問題)
18. [PPTX がスライドマスター表示で開く](#18-pptx-がスライドマスター表示で開く問題)
19. [two_column タイプで左右の内容が表示されない](#19-two_column-タイプで左右の内容が表示されない問題)
20. [未使用プレースホルダーで余白が大きくなる](#20-未使用プレースホルダーで余白が大きくなる問題)

---

## 1. スピーカーノートが消える問題

| 項目     | 内容                                                     |
| -------- | -------------------------------------------------------- |
| **原因** | `create_from_template.py` で notes を設定していなかった  |
| **対策** | PPTX 生成時に notes フィールドを自動設定するよう修正済み |
| **確認** | 生成後に PowerPoint でノートを表示して確認               |
| **状態** | ✅ 修正済み（スクリプト対応）                            |

---

## 2. タイトルが空のスライドが多い問題

| 項目     | 内容                                                            |
| -------- | --------------------------------------------------------------- |
| **原因** | デモ/スクリーンショット用スライドはタイトルプレースホルダーが空 |
| **対策** | `reconstruct_analyzer.py` でスピーカーノートからタイトルを推測  |
| **確認** | content.json 生成時に "Inferred title" ログが出力される         |
| **状態** | ✅ 修正済み（スクリプト対応）                                   |

---

## 3. 画像が見つからない問題

| 項目     | 内容                                                                                             |
| -------- | ------------------------------------------------------------------------------------------------ |
| **原因** | 元 PPTX の画像が抽出されていない、または拡張子が異なる                                           |
| **対策** | `extract_images.py` で事前に画像を抽出 / `create_from_template.py` で .png/.jpg/.jpeg を自動検索 |
| **確認** | PPTX 生成ログで 📷 マークと "[!] Image not found" を確認                                         |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                    |

---

## 4. GitHub Models API レート制限

| 項目     | 内容                                                         |
| -------- | ------------------------------------------------------------ |
| **原因** | 日次 150 リクエスト制限に達する                              |
| **対策** | Localizer エージェントに委託（翻訳は AI エージェントが担当） |
| **確認** | 70 枚以上の PPTX は Localizer エージェント委託推奨           |
| **状態** | ✅ 運用で回避                                                |

---

## 5. 中間ファイルが input/ に保存される問題

| 項目     | 内容                                                                          |
| -------- | ----------------------------------------------------------------------------- |
| **原因** | ワークフロー定義が曖昧だった                                                  |
| **対策** | `input/` はユーザー入力専用 / `output_manifest/` にすべての中間ファイルを保存 |
| **確認** | `input/` に自動生成ファイルがないこと                                         |
| **状態** | ✅ ドキュメント明確化済み                                                     |

---

## 6. 空スライドが生成される問題（two_column）

| 項目     | 内容                                                                                                                 |
| -------- | -------------------------------------------------------------------------------------------------------------------- |
| **原因** | content.json で `two_column` タイプに `left_items`/`right_items` を使用したが、スクリプトは `items` のみ対応していた |
| **対策** | `create_from_template.py` で `left_items` + `right_items` を自動マージして `items` に統合 / 空スライドを検出して警告 |
| **確認** | PPTX 生成ログで "Merged left_items + right_items" が出力される                                                       |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                                        |

---

## 7. 画像が異常に大きく表示される問題

| 項目     | 内容                                                                                                                             |
| -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **原因** | 小さい元画像（アイコン、ロゴ等）に対して `width_percent: 60` 等を指定すると過度に拡大される                                      |
| **対策** | `create_from_template.py` に PIL ベースの画像サイズ検出を追加 / `calculate_max_width_percent()` で自然サイズの 150% を上限に制限 |
| **確認** | PPTX 生成ログで "(capped from X% to Y%)" が出力される                                                                            |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                                                    |

---

## 8. アイコン/ロゴが本文画像として使われる問題

| 項目     | 内容                                                                                                                                |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **原因** | スライドから最大の画像を抽出する際、アイコン/ロゴが選ばれてしまう                                                                   |
| **対策** | `extract_images.py` でアイコン/ロゴを検出してマーク（🔹icon/logo） / `create_from_template.py` で適切な小さいサイズ（15-25%）で配置 |
| **確認** | 抽出/生成ログで "icon/logo detected" が出力される                                                                                   |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                                                       |

---

## 9. position: "center" が無視される問題

| 項目     | 内容                                                                     |
| -------- | ------------------------------------------------------------------------ |
| **原因** | `add_image_to_slide()` が `center` ポジションをサポートしていなかった    |
| **対策** | `create_from_template.py` で `center` を `full` と同様に処理（中央配置） |
| **確認** | 画像が中央に表示されることを視覚確認                                     |
| **状態** | ✅ 修正済み（スクリプト対応）                                            |

---

## 10. 翻訳後に元スライドの参照が不明になる問題

| 項目     | 内容                                                                     |
| -------- | ------------------------------------------------------------------------ | ------------------ |
| **原因** | 要約/統合時に元のスライド番号や視覚要素の位置が分からなくなる            |
| **対策** | Localizer エージェントが翻訳時にスピーカーノートに元スライド情報を追加   |
| **確認** | 翻訳後の notes に元スライド参照が含まれる（フォーマット: `元スライド: #N | レイアウト: xxx`） |
| **状態** | ✅ 修正済み（スクリプト対応）                                            |

---

## 11. items にオブジェクト配列を使用してスキーマエラー

| 項目     | 内容                                                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **原因** | `items` にオブジェクト形式 `{"text": "...", "bullet": true}` を使用したが、`content.schema.json` は文字列配列のみ許容                       |
| **背景** | `replacements.json`（preserve 方式）と `content.json`（reconstruct 方式）で異なるスキーマが存在。ドキュメント間で形式が統一されていなかった |
| **対策** | `common.instructions.md` に「IR スキーマの使い分け」セクションを追加 / `validate_content.py` に `validate_items_format()` を追加            |
| **確認** | `validate_content.py` を IR 生成直後に実行して早期検出                                                                                      |
| **状態** | ✅ 修正済み（スクリプト + ドキュメント対応）                                                                                                |

### 正しい形式

```json
// ✅ OK: content.json の items（string[]）
"items": ["項目1", "項目2", "項目3"]

// ❌ NG: スキーマエラー
"items": [{"text": "項目1", "bullet": true}]
```

> 📖 詳細: [common.instructions.md の「IR スキーマの使い分け」](../.github/instructions/common.instructions.md)

---

## 12. PLAN フェーズで選択肢が指定しづらい問題

| 項目     | 内容                                                                          |
| -------- | ----------------------------------------------------------------------------- |
| **原因** | テンプレートに A, B を割り当て、その他方式に `-` を使用していた               |
| **症状** | 「pptxgenjs を選びたい」時に「2C」のように簡潔に指定できなかった              |
| **対策** | 全方式に連続したアルファベットを割り当てるルールを明文化                      |
| **確認** | テンプレート 2 個 → A, B がテンプレート、C=pptxgenjs, D=create_ja_pptx        |
| **状態** | ✅ 修正済み（plan-phase.instructions.md, AGENTS.md, copilot-instructions.md） |

**修正内容:**

- `plan-phase.instructions.md` に項番ルールを追加
- 入力フォーマット: `{枚数}{方式}` 形式（例: `2A`, `3C`）

---

## 13. まとめスライドがあるのに警告が出る問題

| 項目     | 内容                                                                            |
| -------- | ------------------------------------------------------------------------------- |
| **原因** | `validate_content.py` が `type: "summary"` のみをチェックしていた               |
| **症状** | `type: "content"` + `title: "まとめ"` のスライドを検出できず警告が出た          |
| **対策** | まとめ系キーワード（まとめ/summary/結論/conclusion/おわりに）を検出するよう改善 |
| **確認** | `validate_content.py` を実行し、警告が出ないことを確認                          |
| **状態** | ✅ 修正済み（スクリプト対応）                                                   |

---

## 14. 背景画像がスクリーンショットに重なる問題

| 項目     | 内容                                                                                                 |
| -------- | ---------------------------------------------------------------------------------------------------- |
| **原因** | 英語版 PPTX のスライドマスターに装飾用背景画像（山の風景、ブランドグラフィック等）が埋め込まれていた |
| **症状** | 生成したスライドにスクリーンショットと背景画像が重なって表示される                                   |
| **背景** | Microsoft Ignite 等のイベント用テンプレートには多数のマスターと装飾画像が含まれる                    |
| **対策** | `clean_template.py` でマスター内の PICTURE シェイプを自動削除                                        |
| **確認** | `diagnose_template.py` で事前診断、問題があれば自動クリーニング                                      |
| **状態** | ✅ 修正済み（新規スクリプト追加 + PREPARE_TEMPLATE フェーズ導入）                                    |

### 診断・修正手順

```powershell
# 1. テンプレート診断
python scripts/diagnose_template.py "input/template.pptx"

# 2. 問題があればクリーニング
python scripts/clean_template.py "input/template.pptx" "output_manifest/{base}_clean_template.pptx"

# 3. クリーンテンプレートでPPTX生成
python scripts/create_from_template.py "output_manifest/{base}_clean_template.pptx" ...
```

---

## 15.「この画像は表示できません」エラー

| 項目     | 内容                                                                                                          |
| -------- | ------------------------------------------------------------------------------------------------------------- |
| **原因** | Picture Placeholder にデフォルト画像の blip 参照が埋め込まれていた / 画像追加後に空のプレースホルダーが残った |
| **症状** | スライドに「この画像は表示できません」というプレースホルダーが表示される                                      |
| **背景** | レイアウト内の Picture Placeholder には blip 要素でサンプル画像が埋め込まれていることがある                   |
| **対策** | `create_from_template.py` に `remove_empty_picture_placeholders()` 関数を追加し、画像追加後に自動削除         |
| **確認** | PPTX 生成ログで "[i] Removed N empty picture placeholder(s)" が出力される                                     |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                                 |

### 技術詳細

```python
# 空のPicture Placeholderを検出・削除
def remove_empty_picture_placeholders(slide):
    for shape in slide.shapes:
        if shape.is_placeholder:
            ph_type = str(shape.placeholder_format.type)
            if 'PICTURE' in ph_type:
                # blip参照がなければ空 → 削除
                xml = etree.tostring(shape._element, encoding='unicode')
                if 'blip' not in xml or 'r:embed' not in xml:
                    shape._element.getparent().remove(shape._element)
```

---

## 16. pptxgenjs でスピーカーノートが設定されない問題

| 項目     | 内容                                                                            |
| -------- | ------------------------------------------------------------------------------- |
| **原因** | `create_pptx.js` で `addSignature()` のみでノートを追加し、メインループで未設定 |
| **症状** | 最初と最後のスライドのみノートがあり、中間スライドのノートが空                  |
| **対策** | メインのスライド作成ループ内で `slide.addNotes(slideData.notes)` を追加         |
| **確認** | 生成後に PowerPoint でノートペインを確認                                        |
| **状態** | ✅ 修正済み（create_pptx.js 修正）                                              |

### 修正コード

```javascript
// create_pptx.js のスライド作成ループ内
if (slideData.notes) {
  slide.addNotes(slideData.notes);
}
```

---

## 17. photo スライドが見にくい問題

| 項目       | 内容                                                                                         |
| ---------- | -------------------------------------------------------------------------------------------- |
| **原因**   | photo タイプが Layout 15 (Title - Square Photo) を使用し、タイトル左・画像右の固定配置になる |
| **症状**   | タイトルと画像が離れすぎて余白が大きい / スクリーンショットが小さくて見にくい                |
| **背景**   | `position: center` を指定してもレイアウト構造が優先される                                    |
| **対策 1** | photo タイプに Layout 12 (Title Only) を使用し、画像を大きく中央配置                         |
| **対策 2** | photo タイプを content に変換し、ノートから抽出した説明文を箇条書きとして追加                |
| **確認**   | layouts.json の `photo` マッピングを 12 に変更 / content.json で items を追加                |
| **状態**   | ✅ 運用で対応（content.json 生成時に改善）                                                   |

### 推奨パターン

```json
// Before: 画像だけで何を見せているかわからない
{
  "type": "photo",
  "title": "DSPM ダッシュボード",
  "image": { "path": "images/slide_22.png", "position": "right", "width_percent": 45 }
}

// After: 説明文を追加してわかりやすく
{
  "type": "content",
  "title": "DSPM ダッシュボード",
  "items": [
    "データセキュリティの簡素化",
    "主要なポスチャメトリクス",
    "目標（Objectives）の設定"
  ],
  "image": { "path": "images/slide_22.png", "position": "right", "width_percent": 50 }
}
```

---

## 18. PPTX がスライドマスター表示で開く問題

| 項目       | 内容                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------- |
| **原因**   | テンプレート PPTX の `ppt/viewProps.xml` に `lastView="sldMasterView"` が設定されていた     |
| **症状**   | 生成した PPTX を PowerPoint で開くと、通常の編集画面ではなくスライドマスター表示で開く      |
| **背景**   | python-pptx はテンプレートの viewProps.xml をそのままコピーするため、メタデータが継承される |
| **対策 1** | `diagnose_template.py` で `check_view_props()` を追加し、事前検出可能に                     |
| **対策 2** | `create_from_template.py` で `_normalize_view_settings()` を追加し、保存後に自動修正        |
| **確認**   | 生成ログで "Normalized view settings" が表示されることを確認                                |
| **状態**   | ✅ 修正済み（スクリプト対応）                                                               |

### 技術詳細

PPTX 内部の `ppt/viewProps.xml` には以下のような設定が含まれる:

```xml
<!-- NG: スライドマスター表示で開く -->
<p:viewPr lastView="sldMasterView" xmlns:p="...">

<!-- OK: 通常のスライド表示で開く -->
<p:viewPr lastView="sldView" xmlns:p="...">
```

### 修正コード（create_from_template.py 内）

```python
def _normalize_view_settings(pptx_path: str) -> bool:
    """PPTX 保存後に viewProps.xml を修正して通常表示で開くようにする"""
    import zipfile
    import shutil

    temp_path = pptx_path + ".tmp"
    modified = False

    with zipfile.ZipFile(pptx_path, 'r') as zin:
        with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "ppt/viewProps.xml":
                    content = data.decode('utf-8')
                    if 'lastView="sldMasterView"' in content:
                        content = content.replace('lastView="sldMasterView"', 'lastView="sldView"')
                        data = content.encode('utf-8')
                        modified = True
                zout.writestr(item, data)

    if modified:
        shutil.move(temp_path, pptx_path)
        print("    [✓] Normalized view settings (sldMasterView → sldView)")
    else:
        os.remove(temp_path)

    return modified
```

### 診断コマンド

```powershell
# テンプレートの viewProps 設定を確認
python scripts/diagnose_template.py "templates/template.pptx"

# 生成済み PPTX を手動で確認
python -c "import zipfile; z=zipfile.ZipFile('output.pptx'); print(z.read('ppt/viewProps.xml').decode())"
```

---

## 19. two_column タイプで左右の内容が表示されない問題

| 項目     | 内容                                                                                                                                                      |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **原因** | `create_ja_pptx.py` と `create_pptx.js` が `two_column` タイプを個別処理していなかった                                                                    |
| **症状** | `type: "two_column"` のスライドでタイトルのみ表示され、`left_items` / `right_items` の内容が空になる                                                      |
| **背景** | content.json では `two_column` タイプに `left_title`, `left_items`, `right_title`, `right_items` を使用するが、これらのフィールドを読み取る処理がなかった |
| **対策** | `create_ja_pptx.py` に `add_two_column_slide()` 関数を追加 / `create_pptx.js` に `addTwoColumnSlide()` 関数を追加                                         |
| **確認** | PPTX 生成後に 2 列レイアウトのスライドで左右の内容が表示されることを確認                                                                                  |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                                                                             |

### content.json での正しい形式

```json
{
  "type": "two_column",
  "title": "2つのスタイル比較",
  "left_title": "Sentry",
  "left_items": ["約800行 / 26KB", "詳細・網羅的", "リファレンス型"],
  "right_title": "Temporal",
  "right_items": ["約100行", "シンプル・構造化", "指示型"],
  "notes": "SentryとTemporalで対照的なアプローチ。"
}
```

### 修正対象スクリプト

| スクリプト                | 追加関数                                                             |
| ------------------------- | -------------------------------------------------------------------- |
| `create_ja_pptx.py`       | `add_two_column_slide()`                                             |
| `create_pptx.js`          | `addTwoColumnSlide()`                                                |
| `create_from_template.py` | 既存対応済み（`left_items` + `right_items` を `items` に自動マージ） |

> 📝 **注意**: `create_from_template.py` は既存のテンプレートレイアウトを使用するため、`left_items` と `right_items` を自動的に `items` に統合して処理します。これは TROUBLESHOOTING #6 で対応済みです。

---

## クイックリファレンス: よくある問題と解決策

| 症状                               | 原因                     | 解決策                                   |
| ---------------------------------- | ------------------------ | ---------------------------------------- |
| PPTX に画像がない                  | 画像未抽出               | `extract_images.py` を先に実行           |
| 空スライドがある                   | items がない             | `validate_content.py` で検証             |
| 画像がぼやける                     | 小画像を拡大             | `width_percent` を下げる（自動制限あり） |
| スキーマエラー                     | items がオブジェクト配列 | `string[]` に変更                        |
| API レート制限                     | 大量翻訳                 | Localizer エージェントに委託             |
| ノートが消えた                     | 古いスクリプト           | 最新版に更新                             |
| 選択肢が指定しづらい               | 項番が不連続             | A,B,C... で連続割当                      |
| まとめがあるのに警告               | type 検出のみ            | タイトルキーワードも検出（修正済み）     |
| **背景画像が重なる**               | マスター内装飾画像       | `clean_template.py` でクリーニング       |
| **画像表示できませんエラー**       | 空の Picture Placeholder | 自動削除機能追加済み                     |
| **pptxgenjs でノートなし**         | addNotes 未呼び出し      | create_pptx.js 修正済み                  |
| **photo スライドが見にくい**       | レイアウト固定           | Layout 12 使用 or content に変換         |
| **スライドマスター表示で開く**     | viewProps.xml 設定継承   | `_normalize_view_settings()` で自動修正  |
| **two_column が空で表示**          | left/right_items 未対応  | スクリプト修正済み                       |
| **未使用プレースホルダーで余白**   | Body PH が空のまま残る   | 自動削除機能追加済み                     |
| **セクションスライドが空に見える** | subtitle 未設定          | subtitle フィールドを必須化              |

---

## 20. 未使用プレースホルダーで余白が大きくなる問題

| 項目     | 内容                                                                                                                                         |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **症状** | テンプレートに Body/Content プレースホルダーがあるレイアウトを使用し、items を渡さなかった場合、空のプレースホルダーが残り余白が大きく見える |
| **原因** | 使われていないプレースホルダーが削除されずに残っていた                                                                                       |
| **対策** | (1) コンテンツなし時に自動でシンプルなレイアウト（title_only/blank）を選択、(2) それでも残る空の Body PH を自動削除                          |
| **確認** | PPTX 生成ログで "[i] No content → using simpler layout" や "[i] Removed N empty body placeholder(s)" が出力される                            |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                                                                |

### 改善内容

1. **`analyze_template.py`**: `title_only` レイアウトカテゴリを `layout_mapping` に追加
2. **`create_from_template.py`**:
   - `remove_empty_body_placeholders()` 関数を追加（空の Body/Content PH を削除）
   - コンテンツ量に応じた最適レイアウト自動選択ロジックを追加
   - `title_only`, `blank`, `photo` レイアウトの自動検出を追加

### 自動選択ロジック

| 条件                                      | 選択されるレイアウト     |
| ----------------------------------------- | ------------------------ |
| `type: "content"` + items なし + 画像なし | `title_only` or `blank`  |
| `type: "photo"` + items なし + 画像あり   | `photo` or `blank`       |
| 通常のコンテンツあり                      | 元のレイアウトマップ通り |

---

> 💡 **新しい問題が発生したら**: このファイルに追記してください。

---

## 21. 画像がスライド右端にはみ出す問題

| 項目     | 内容                                                                                                            |
| -------- | --------------------------------------------------------------------------------------------------------------- |
| **症状** | `image.position: "right"` で配置した画像がスライドの右端からはみ出す                                            |
| **原因** | スライド幅を 13.333 インチ（標準サイズ）でハードコードしていた。別サイズのテンプレート（例：10.0 インチ）で破綻 |
| **対策** | `prs.slide_width.inches` で動的にスライドサイズを取得し、全ての計算に適用                                       |
| **確認** | 異なるサイズのテンプレートでも画像がはみ出さない                                                                |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                                   |

### 改善内容

`create_from_template.py` の `add_image_to_slide()` 関数を修正：

```python
# ❌ 修正前: ハードコード
slide_width = 13.333
img_left = Inches(slide_width - margin) - img_width

# ✅ 修正後: 動的取得
slide_width_inches = prs.slide_width.inches
slide_height_inches = prs.slide_height.inches
img_left = Inches(slide_width_inches - margin) - img_width
```

### 影響範囲

- 画像の `position: "right"` 配置
- 画像の `position: "bottom"` 配置
- コードブロックの配置
- コンテンツエリアの高さ計算

---

## 22. コードブロックがスライド下部にはみ出す問題

| 項目     | 内容                                                                                                        |
| -------- | ----------------------------------------------------------------------------------------------------------- |
| **症状** | `code` フィールドで追加したコードブロックがスライドの下端からはみ出す                                       |
| **原因** | コードブロックの位置（`code_top = 4.5 インチ`）と高さ（`code_height = 2.0 インチ`）がハードコードされていた |
| **対策** | スライド高さに対する比率で動的に計算（60% 位置から開始、32% の高さ）                                        |
| **確認** | 小さいテンプレート（5.625 インチ高）でもはみ出さない                                                        |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                               |

### 改善内容

```python
# ❌ 修正前: ハードコード
code_top = Inches(4.5)
code_height = Inches(2.0)

# ✅ 修正後: スライド高さに応じた動的計算
slide_height = prs.slide_height.inches
code_top = Inches(slide_height * 0.6)      # 60% の位置
code_height = Inches(slide_height * 0.32)  # 32% の高さ
```

---

## 23. fetch_webpage で画像 URL が取得できない問題

| 項目     | 内容                                                                         |
| -------- | ---------------------------------------------------------------------------- |
| **症状** | `fetch_webpage` ツールで Web 記事を取得しても、記事内の画像 URL が含まれない |
| **原因** | ツールの仕様として画像 URL は返さない場合がある                              |
| **対策** | `curl` で HTML ソースを取得し、正規表現で画像 URL を抽出する                 |
| **確認** | 記事に画像があるか `curl -s $url \| Select-String '<img'` で事前確認         |
| **状態** | ⚠️ ワークフロー対応（ツール制限のため）                                      |

### 対応手順

```powershell
# 1. HTML ソースを取得
$html = curl -s $url

# 2. 画像URLを正規表現で抽出
$imageUrls = [regex]::Matches($html, 'https://[^"]+\.(png|jpg|jpeg|gif|webp)') |
    ForEach-Object { $_.Value } | Select-Object -Unique

# 3. 画像をダウンロード
foreach ($imgUrl in $imageUrls) {
    curl -s -o "images/${base}/${i}_image.png" $imgUrl
}
```

**PLAN フェーズで確認**: Web ソースの場合、必ず画像の有無を事前確認すること。

---

## 24. content.json の code フィールドが反映されない問題

| 項目     | 内容                                                                                              |
| -------- | ------------------------------------------------------------------------------------------------- |
| **症状** | content.json に `code` フィールドを追加しても、PPTX にコードブロックが表示されない                |
| **原因** | `create_from_template.py` の `add_slide_from_layout()` が `code` パラメータを受け取っていなかった |
| **対策** | 関数に `code` パラメータを追加し、暗色背景 + Consolas フォントでコードブロックを描画              |
| **確認** | 生成ログに `💻` マークが表示される                                                                |
| **状態** | ✅ 修正済み（スクリプト対応）                                                                     |

### 改善内容

1. `add_slide_from_layout()` に `code: Optional[str] = None` パラメータを追加
2. コードブロックのスタイル:
   - 背景色: `RGBColor(40, 44, 52)` （ダークテーマ）
   - フォント: Consolas, 11pt
   - 文字色: `RGBColor(171, 178, 191)` （ライトグレー）
3. 位置は items がある場合は下部、ない場合は中央に自動調整

---

## 25. セクションスライドが空っぽに見える問題

| 項目     | 内容                                                                               |
| -------- | ---------------------------------------------------------------------------------- |
| **症状** | `type: "section"` のスライドがタイトルのみで、本文が空っぽに見える                 |
| **原因** | セクションスライドは本来タイトルのみのレイアウトだが、文脈がないと意味が伝わらない |
| **対策** | `subtitle` フィールドを必須化し、セクションの概要や次の内容を記載                  |
| **確認** | PPTX 生成後、セクションスライドにサブタイトルが表示される                          |
| **状態** | ✅ ルール化済み（ドキュメント対応）                                                |

### 問題例

```json
// ❌ NG: タイトルのみで空っぽに見える
{
  "type": "section",
  "title": "MCP サーバーの開発とデプロイ"
}

// ✅ OK: subtitle でセクションの概要を追加
{
  "type": "section",
  "title": "MCP サーバーの開発とデプロイ",
  "subtitle": "VS Code で開発し Azure Container App にデプロイ",
  "notes": "このセクションでは..."
}
```

### 推奨される subtitle の書き方

| パターン             | 例                                                |
| -------------------- | ------------------------------------------------- |
| 内容の要約           | "VS Code で開発し Azure Container App にデプロイ" |
| これから説明すること | "認証フローと必要な設定項目を解説"                |
| キーワード列挙       | "Entra ID / アプリ登録 / スコープ設定"            |
| ステップ番号         | "Step 2 of 4: 認証設定"                           |

### 更新されたドキュメント

- `.github/copilot-instructions.md`: 必須ルールに追加
- `.github/instructions/quality-guidelines.instructions.md`: 詳細ルール追加
- `workspace/content.example.json`: section スライドの例追加
