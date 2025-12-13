# output_manifest/

PPTX 生成の中間ファイル保存フォルダ。

## 構造

```
output_manifest/
├── {base}_content.json      # 元 PPTX から抽出したコンテンツ
├── {base}_content_ja.json   # 翻訳後のコンテンツ
├── {base}_inventory.json    # シェイプ一覧（preserve 方式）
├── {base}_article.json      # Web 記事の取得結果
└── {base}_working.pptx      # 作業用 PPTX
```

## 命名規則

| パターン                 | 説明                        |
| ------------------------ | --------------------------- |
| `{base}_content.json`    | IR 形式のコンテンツ（原文） |
| `{base}_content_ja.json` | 翻訳済みコンテンツ          |
| `{base}_inventory.json`  | シェイプ分析結果            |
| `{base}_article.json`    | API から取得した記事データ  |
| `qiita_*.json`           | Qiita API レスポンス        |

## 使用ツール

- `scripts/reconstruct_analyzer.py` - PPTX → content.json
- Localizer Agent - content.json → content_ja.json
- `scripts/extract_shapes.py` - PPTX → inventory.json

## 注意

- このフォルダの内容は `.gitignore` で除外されています
- 最終成果物は `output_ppt/` に出力されます
