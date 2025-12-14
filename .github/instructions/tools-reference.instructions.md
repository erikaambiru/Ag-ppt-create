# ツール使用ルール

## 方式選定

| 用途              | 推奨方式                                              | 推奨度     | 備考                 |
| ----------------- | ----------------------------------------------------- | ---------- | -------------------- |
| 英語 PPTX→ 日本語 | `reconstruct_analyzer.py` + `create_from_template.py` | ⭐⭐⭐⭐⭐ | 最推奨、マスター継承 |
| テンプレート利用  | `analyze_template.py` + `create_from_template.py`     | ⭐⭐⭐⭐⭐ | 最推奨、デザイン継承 |
| 白紙から新規作成  | `create_ja_pptx.py`                                   | ⭐⭐⭐⭐   | シンプルできれい     |
| コード/技術内容多 | カスタム JS (pptxgenjs)                               | ⭐⭐⭐⭐   | コードブロック向け   |

### 実験的・非推奨方式

| 方式     | 状態             | 理由                                                            |
| -------- | ---------------- | --------------------------------------------------------------- |
| preserve | **experimental** | 図・グラフで崩れやすい（今後改善予定）→ 現在は reconstruct 推奨 |
| html     | **deprecated**   | デザイン品質が低い → template 方式を使用                        |

## 共通ツール

### 分類・抽出

- `classify_input.py`: 入力分類・方式判定 → classification.json 出力
- `reconstruct_analyzer.py`: 英語版 PPTX → content.json 変換（スライドタイプ自動判定、ノート抽出、タイトル推測）
  - `--classification` オプションで classification.json を参照可能
- `extract_images.py`: PPTX から画像を抽出 → images/slide\_{nn}.png/jpg

### テンプレート処理

- `analyze_template.py`: テンプレートのレイアウト分析 → layouts.json 生成（初回のみ）
- `diagnose_template.py`: テンプレート品質診断（背景画像、壊れた参照等）
- `clean_template.py`: テンプレートから背景画像・不要要素を削除

### PREPARE_TEMPLATE フェーズ

外部テンプレート（特に英語版 PPTX）を使用する場合、以下の問題が発生しうる:

| 問題                        | 症状                             | 対処                           |
| --------------------------- | -------------------------------- | ------------------------------ |
| マスター内背景画像          | 生成スライドに山の風景等が重なる | PICTURE シェイプを削除         |
| Picture Placeholder の blip | 「この画像は表示できません」表示 | blip 参照を削除 or PH 自体削除 |
| 埋め込みフォント不足        | フォント置換警告                 | 代替フォント指定               |
| 壊れた外部リンク            | リンク切れエラー                 | 外部参照を削除                 |
| viewProps.xml 設定継承      | スライドマスター表示で開く       | 自動正規化（BUILD 時）         |

**診断・クリーニング手順:**

```powershell
# テンプレート診断
python scripts/diagnose_template.py "input/template.pptx"

# 問題があればクリーニング
python scripts/clean_template.py "input/template.pptx" "output_manifest/${base}_clean_template.pptx"
```

### 変換

- `summarize_content.py`: 全体把握 → 要約再構成

> 💡 翻訳は Localizer エージェントが担当します（スクリプトではなく AI 判断）

### 検証

- `validate_content.py`: content.json のスキーマ検証・空コンテンツ検出・画像パス検証
- `validate_pptx.py`: PPTX 検証（スライド数一致・ノート存在・画像配置）
- `check_overflow.py`: bbox 事前検証

### 並列実行

- `extract_parallel.ps1`: EXTRACT フェーズの並列実行（analyze_template + extract_images + reconstruct_analyzer）
  - 使用例: `.\scripts\extract_parallel.ps1 -InputPptx "input/presentation.pptx" -Base "20251214_example"`

### 生成

- `create_from_template.py`: content.json + テンプレート → PPTX
  - **検証機能**: `type='content'` に `items`/`bullets` がないスライドを検出し終了コード 1 で中断
  - **空プレースホルダー削除**: 画像追加後に空の Picture Placeholder を自動削除
  - `--force` で警告付き強制生成可
- `create_ja_pptx.py`: JSON→ 新規 PPTX（python-pptx）

## preserve 方式専用ツール（⚠️ experimental）

> 現在は reconstruct 方式を推奨しますが、preserve 方式は今後改善予定です。

- `reorder_slides.py`: 0 始まり index
- `extract_shapes.py`: inventory/analysis 出力、編集不可
- `apply_content.py`: replacements + slides_to_keep を適用

## 非推奨ツール

- ~~`extract_main_slides.py`~~: 機械的スライド間引き（文脈を失う）
- ~~`convert_html.js/multi`~~: HTML ベース方式用（非推奨）

---

## 英語版 PPTX 日本語化フロー（reconstruct 方式）★ 推奨

```powershell
$base = "20251213_purview_ignite"
$input = "input/BRK252_presentation.pptx"

# 0. ★ テンプレート診断・クリーニング（外部テンプレート使用時は必須）
python scripts/diagnose_template.py $input
# 問題があれば:
python scripts/clean_template.py $input "output_manifest/${base}_clean_template.pptx"
$template = "output_manifest/${base}_clean_template.pptx"
# 問題がなければ:
$template = $input

# 1. レイアウト分析（初回のみ）
python scripts/analyze_template.py $template

# 2. ★ 画像抽出（必須）
python scripts/extract_images.py $input "images"

# 3. コンテンツ抽出 → content.json
python scripts/reconstruct_analyzer.py $input "output_manifest/${base}_content.json"

# 4. 翻訳（Localizer エージェントに委託）
# Localizer エージェントが content.json を翻訳します
# → output_manifest/${base}_content_ja.json

# 5. PPTX 再構成
python scripts/create_from_template.py $input "output_manifest/${base}_content_ja.json" "output_ppt/${base}.pptx"

# 6. PowerPoint で確認
Start-Process "output_ppt/${base}.pptx"
```

## 画像取得ルール（Web ソース時）

Web ソース（Qiita, Zenn, ブログ等）からの PPTX 生成では、**画像取得を最初に行う**。

### ⚠️ 重要: fetch_webpage の制限

`fetch_webpage` ツールは**画像 URL を返さない場合がある**。以下の手順で別途取得すること：

```powershell
$base = "20251212_example_blog"
$url = "https://zenn.dev/xxx/articles/yyy"

# 1. HTMLソースを取得
$html = curl -s $url

# 2. 画像URLを正規表現で抽出（storage.googleapis.com や qiita-image-store 等）
$imageUrls = [regex]::Matches($html, 'https://[^"]+\.(png|jpg|jpeg|gif|webp)') |
    ForEach-Object { $_.Value } |
    Select-Object -Unique

# 3. 画像保存ディレクトリ作成
New-Item -ItemType Directory -Path "images/${base}" -Force

# 4. 画像をダウンロード
$i = 1
foreach ($imgUrl in $imageUrls) {
    $ext = [System.IO.Path]::GetExtension($imgUrl) -replace '\?.*$', ''
    curl -s -o "images/${base}/$('{0:D2}' -f $i)_image$ext" $imgUrl
    $i++
}
```

### コードブロック抽出ルール

記事内のコードブロックは content.json の `code` フィールドに格納する：

```json
{
  "type": "content",
  "title": "実装例",
  "items": ["ポイント1", "ポイント2"],
  "code": "<button hx-get=\"/api/data\">取得</button>"
}
```

**対応状況:**

| 方式                         | コードブロック対応 | 備考                         |
| ---------------------------- | ------------------ | ---------------------------- |
| `create_from_template.py`    | ✅ 対応済み        | 暗色背景 + Consolas フォント |
| `create_pptx.js` (pptxgenjs) | ✅ 対応済み        | ネイティブ対応               |
| `create_ja_pptx.py`          | ⚠️ 要追加          | 将来対応予定                 |

### 画像・コード配置ルール

| 配置   | 画像フィールド             | コードフィールド       |
| ------ | -------------------------- | ---------------------- |
| 右寄せ | `image.position: "right"`  | -                      |
| 下部   | `image.position: "bottom"` | 箇条書きの下に自動配置 |
| フル   | `image.position: "full"`   | -                      |

- **保存先**: `images/{base}/` 配下に統一
- **命名規則**: `{連番}_{内容}.png`
- **配置**: 関連スライドに直接配置（Appendix ではなく）
- **type**: 画像スライドは `type: "photo"` を使用

## テンプレート新規生成フロー

```powershell
# テンプレートを動的に取得（先頭のファイルを使用）
$template = (Get-ChildItem -Path "templates" -Filter "*.pptx" | Select-Object -First 1).BaseName
$base = "20251212_example_blog"

# 1. layouts.json がなければ分析
if (-not (Test-Path "output_manifest/${template}_layouts.json")) {
    python scripts/analyze_template.py "templates/${template}.pptx"
}

# 2. 画像取得（Web ソースの場合）
New-Item -ItemType Directory -Path "images/${base}" -Force
curl -s -o "images/${base}/01_diagram.png" "{extracted_image_url}"

# 3. content.json 作成（画像パスを含める）

# 4. PPTX 生成
python scripts/create_from_template.py "templates/${template}.pptx" "output_manifest/${base}_content.json" "output_ppt/${base}.pptx"
```

## Web ソースからの PPTX 生成フロー（全方式共通）

```
1. 記事取得（API or fetch）
     ↓
2. ★ 画像URL抽出 & ダウンロード（images/{base}/）
     ↓
3. 枚数計算: 基本枚数 + 画像枚数
     ↓
4. content.json 作成（type: "photo" で画像配置）
     ↓
5. PPTX 生成
```

**フロー遵守**: 画像取得をスキップして後から追加するのは禁止。
