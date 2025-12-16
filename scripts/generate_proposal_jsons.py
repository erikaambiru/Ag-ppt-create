import json
import os

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {path}")

# Common Slides
title_slide = {
    "type": "title",
    "title": "Azure 運用担当者・SIer 様へ：GitHub Copilot がもたらす運用業務の変革と活用メリット",
    "subtitle": "運用・構築・ドキュメント作成を支援するAIパートナー",
    "notes": "こんにちは、アーキテクトのやまぱんです。\n本日は、アプリ開発者ではない運用担当者やSIerの皆様に向けて、GitHub Copilotの活用メリットをお話しします。"
}

agenda_slide = {
    "type": "agenda",
    "title": "本日の流れ",
    "items": [
        "背景：なぜ運用者・SIerにCopilotが必要か",
        "GitHub Copilotの進化（ChatからMCPへ）",
        "デモンストレーション",
        "活用メリット（IaC、スクリプト、ドキュメント、Office連携）",
        "未来の運用（Azure MCP）",
        "安全性とガバナンス"
    ],
    "notes": "本日のアジェンダです。まずは背景から入り、Copilotの最新機能、そして具体的な活用シナリオをご紹介します。"
}

background_slide = {
    "type": "content",
    "title": "背景：「コードを書かない」運用者・SIer こそ活用すべき理由",
    "items": [
        "「Copilotはプログラマ用」という誤解",
        "運用者・SIerの業務は「テキスト（言語）」を扱う作業が多い",
        "設計書、構成図、スクリプト、IaC、ログ解析など",
        "Copilotは「自然言語」も理解する強力なパートナー"
    ],
    "notes": "「GitHub Copilotはプログラマがコード補完をするためのツール」と誤解されていませんか？\n実は、設計書やパラメータシート、構成図、スクリプトなど、私たちの業務の多くは「テキスト」を扱います。\nCopilotは自然言語を理解するため、これらの定型作業を強力に支援してくれます。"
}

what_is_copilot_slide = {
    "type": "content",
    "title": "GitHub Copilot とは？",
    "subtitle": "「補完」から「エージェント」へ",
    "items": [
        "Ghost Text（コード補完）だけではない",
        "対話型AI (Copilot Chat) で文脈を理解した回答",
        "エージェントとして自律的に支援する機能へ進化"
    ],
    "notes": "Copilotは単なるコード補完ツールから、対話型AI、そして自律的なエージェントへと進化しています。"
}

evolution_slides = [
    {
        "type": "content",
        "title": "進化の軌跡 1: 対話型 AI (Copilot Chat)",
        "items": [
            "エディタの中でAIと対話が可能",
            "「このコードの意味は？」「より良い実装方法は？」",
            "開いているファイルの文脈を理解して回答"
        ],
        "notes": "まずはCopilot Chatです。ChatGPTのように対話が可能で、開いているファイルを理解して回答してくれます。"
    },
    {
        "type": "content",
        "title": "進化の軌跡 2: エージェントモード (Agent Mode)",
        "items": [
            "「回答者」から「自律的な調査員」へ",
            "@workspace: プロジェクト全体を横断検索・理解",
            "ターミナル連携: エラーログを読み取り修正案を提示"
        ],
        "notes": "次にエージェントモードです。ユーザーが詳細を説明しなくても、@workspaceを使ってプロジェクト全体から情報を探し出してくれます。"
    },
    {
        "type": "content",
        "title": "進化の軌跡 3: エージェントワークフロー (Agent Workflow)",
        "items": [
            "「作業者」として複数ステップを実行",
            "Copilot Edits: ファイル作成、コード記述、テスト実行まで",
            "複雑なタスクをプランニングして実行"
        ],
        "notes": "さらにエージェントワークフローでは、Copilotが作業者として複数のステップを自律的に実行します。"
    },
    {
        "type": "content",
        "title": "進化の軌跡 4: Model Context Protocol (MCP)",
        "items": [
            "VS Codeの外側にあるデータやツールと連携",
            "外部データ連携: 社内DB、Azureリソース、監視ログ",
            "ツール実行: VM再起動、チケット更新など",
            "「システム全体のオペレーター」へ進化"
        ],
        "notes": "そして最新のMCPです。これにより、VS Codeの外にあるAzure環境や社内システムとも連携できるようになります。"
    }
]

demo_slide = {
    "type": "section",
    "title": "Demo: 進化した Copilot の実演",
    "subtitle": "Agent Mode / Copilot Edits / MCP",
    "notes": "百聞は一見に如かず。実際の動きをご覧ください。\n1. Agent Modeでの調査\n2. Copilot Editsでの修正\n3. MCPによるAzure操作"
}

merit1_slide = {
    "type": "content",
    "title": "活用メリット 1: インフラコード (IaC) 作成の効率化",
    "items": [
        "リソース定義の暗記やドキュメント検索が不要に",
        "コメントで指示するだけで雛形を作成",
        "Excelパラメータシートからの生成も有効"
    ],
    "code": "// 東日本リージョンに、LRS のストレージアカウントを作成する\n// 名前はユニークになるようにランダムな文字列を含める\nresource storage 'Microsoft.Storage/storageAccounts@2021-04-01' = ...",
    "notes": "BicepやTerraformの記述が劇的に効率化されます。コメントを書くだけでコードが生成されるため、ドキュメントを行き来する時間が削減されます。"
}

merit2_slide = {
    "type": "content",
    "title": "活用メリット 2: 「非定型」なスクリプト作成の負荷軽減",
    "items": [
        "頻度は低いが手作業では困難な処理を自動化",
        "PowerShell/Azure CLIの構文を記憶していなくてもOK",
        "ログ調査（正規表現）やJSON整形も支援"
    ],
    "code": "# 30日以上更新されていない Blob をすべて削除する\nGet-AzStorageBlob -Container \"logs\" | Where-Object ...",
    "notes": "たまにしか書かないスクリプトや、複雑なログ解析コマンドも、やりたいことを伝えるだけで生成してくれます。"
}

merit3_slide = {
    "type": "content",
    "title": "活用メリット 3: ドキュメント作成の自動化",
    "items": [
        "SIer業務の多くを占めるドキュメント作成を効率化",
        "AG-Diagram Maker: テキストから構成図を生成（編集可能）",
        "Ag-ppt-create: MarkdownからPowerPointを生成"
      ],
      "notes": "実はドキュメント作成こそ効果が高いポイントです。図やスライドの作成すら自動化するツールが登場しています。"
    }

merit4_slide = {
    "type": "content",
    "title": "活用メリット 4: レガシー資産の「解読」と「継承」",
    "items": [
        "前任者の複雑なスクリプトを解読",
        "@workspace でリポジトリ全体を検索",
        "「過去のプロジェクト規約」に沿った回答も可能",
        "新人教育や引き継ぎに絶大な効果"
      ],
      "notes": "ブラックボックス化したレガシー資産の解読や、プロジェクト固有のルールの継承にも役立ちます。"
}

merit5_slide = {
    "type": "content",
    "title": "活用メリット 5: Excel / PowerPoint 設計書の直接理解",
    "items": [
        "Officeドキュメントもコンテキストとして理解",
        "パラメータシート(Excel)からコード生成",
        "要件定義書からシーケンス図などを生成"
    ],
    "notes": "ExcelやPowerPointの仕様書を読み込ませて、そこからコードや図を生成することも可能になりつつあります。"
}

merit6_slide = {
    "type": "content",
    "title": "活用メリット 6: MCP による Azure 運用・管理の自動化",
    "items": [
        "環境情報の即時把握と資料化（ポータル確認不要）",
        "運用操作の自動化（VM起動・停止、リソース削除）",
        "チャットで指示 → コマンド提案 → 実行"
      ],
      "notes": "MCPを使えば、Azure環境の情報をチャットで取得して表にまとめたり、リソース操作を行ったりできます。"
}

safety_slide = {
    "type": "content",
    "title": "懸念への回答：安全性とガバナンス",
    "items": [
        "Human in the Loop: 勝手にコマンドを実行しない（必ず承認）",
        "データ保護: プロンプトやコードは学習に利用されない",
        "エンタープライズレベルのセキュリティ"
      ],
      "notes": "「勝手に実行されないか」「情報流出しないか」という懸念に対しては、Human in the Loopの原則と、学習利用なしのデータ保護ポリシーで対応しています。"
}

summary_slide = {
    "type": "content",
    "title": "まとめ：まずは VS Code の導入から",
    "items": [
        "Copilotは「運用・構築・ドキュメント作成」のパートナー",
        "アプリ開発者でなくても導入効果は絶大",
        "今日から「AIとのペア運用」を始めましょう"
      ],
      "notes": "まずはVS Codeをインストールし、Copilotを有効にすることから始めてみてください。"
}

ref_slide = {
    "type": "content",
    "title": "参考リンク",
    "items": [
        "AG-Diagram Maker - GitHub",
        "Ag-ppt-create - GitHub"
      ],
      "notes": "本日ご紹介したツールのリンクです。"
}

# Standard Content
standard_slides = [
    title_slide, agenda_slide, background_slide, what_is_copilot_slide,
    *evolution_slides, demo_slide,
    merit1_slide, merit2_slide, merit3_slide, merit4_slide, merit5_slide, merit6_slide,
    safety_slide, summary_slide, ref_slide
]

# Detailed Content (Splitting some slides)
merit2_detailed_1 = {
    "type": "content",
    "title": "活用メリット 2: 「非定型」なスクリプト作成の負荷軽減",
    "items": [
        "頻度は低いが手作業では困難な処理を自動化",
        "PowerShell/Azure CLIの構文を記憶していなくてもOK",
        "「30日以上更新がないBlobを削除」など自然言語で指示"
    ],
    "code": "# 30日以上更新されていない Blob をすべて削除する\nGet-AzStorageBlob -Container \"logs\" | Where-Object ...",
    "notes": "たまにしか書かないスクリプトも、やりたいことを伝えるだけで生成してくれます。"
}
merit2_detailed_2 = {
    "type": "content",
    "title": "活用メリット 2: ログ調査やJSON整形も支援",
    "items": [
        "複雑な正規表現によるログ抽出",
        "Azure CLIのJSON出力をCSVに変換",
        "jqコマンドやワンライナーを即座に生成"
    ],
    "notes": "ログ解析やデータ整形といった、地味ですが時間のかかる作業も効率化できます。"
}

merit3_detailed_1 = {
    "type": "content",
    "title": "活用メリット 3: ドキュメント作成の自動化",
    "items": [
        "SIer業務の多くを占めるドキュメント作成を効率化",
        "本質的な設計や思考に集中し、作業はAIに任せる"
    ],
    "notes": "ドキュメント作成こそ効果が高いポイントです。"
}
merit3_detailed_2 = {
    "type": "content",
    "title": "活用メリット 3: 図やスライドの自動生成ツール",
    "items": [
        "AG-Diagram Maker: テキストから構成図を生成（編集可能）",
        "Ag-ppt-create: MarkdownからPowerPointを生成",
        "「いつものテンプレート」で自動化"
    ],
    "notes": "図やスライドの作成すら自動化するツールが登場しています。"
}

merit5_detailed_1 = {
    "type": "content",
    "title": "活用メリット 5: Excel パラメータシートからの生成",
    "items": [
        "ExcelのパラメータシートをCopilotに読み込ませる",
        "「このシートの内容でTerraformを書いて」",
        "変数の定義漏れやコピペミスを防止"
    ],
    "notes": "Excelの仕様書を読み込ませて、そこからコードを生成することが可能です。"
}
merit5_detailed_2 = {
    "type": "content",
    "title": "活用メリット 5: 既存資料からの図解生成",
    "items": [
        "要件定義書(Word/Excel)の通信フローを理解",
        "Mermaidでシーケンス図を描画",
        "テキスト情報を人間が理解しやすい図に変換"
    ],
    "notes": "テキスト情報を図に変換する作業も、AIと一緒なら一瞬です。"
}

merit6_detailed_1 = {
    "type": "content",
    "title": "活用メリット 6: 環境情報の即時把握と資料化 (MCP)",
    "items": [
        "「現在の検証環境のリソース一覧を表にして」",
        "Azureに接続し、最新情報を取得してMarkdown表を作成",
        "ポータル確認・キャプチャ・転記作業が不要に"
    ],
    "notes": "MCPを使えば、Azure環境の情報をチャットで取得して表にまとめることができます。"
}
merit6_detailed_2 = {
    "type": "content",
    "title": "活用メリット 6: 運用操作の自動化 (MCP)",
    "items": [
        "「開発用VMを起動して」「リソースグループを削除して」",
        "チャットで指示 → コマンド提案 → 実行",
        "運用オペレーションをチャットから実行可能"
    ],
    "notes": "リソース操作もチャットから行えます。"
}

safety_detailed_1 = {
    "type": "content",
    "title": "懸念への回答 1: Human in the Loop",
    "items": [
        "AIが勝手にコマンドを実行することはない",
        "必ず「このコマンドを実行しますか？」と確認",
        "承認ボタンを押す権限と責任は人間にある"
    ],
    "notes": "「勝手に実行されないか」という懸念に対しては、Human in the Loopの原則で対応しています。"
}
safety_detailed_2 = {
    "type": "content",
    "title": "懸念への回答 2: データ保護とプライバシー",
    "items": [
        "プロンプトやコードスニペットは学習に利用されない",
        "入力データは暗号化され保護される",
        "機密情報が外部に流出することはない"
    ],
    "notes": "「情報流出しないか」という懸念に対しては、学習利用なしのデータ保護ポリシーで対応しています。"
}

detailed_slides = [
    title_slide, agenda_slide, background_slide, what_is_copilot_slide,
    *evolution_slides, demo_slide,
    merit1_slide, 
    merit2_detailed_1, merit2_detailed_2,
    merit3_detailed_1, merit3_detailed_2,
    merit4_slide,
    merit5_detailed_1, merit5_detailed_2,
    merit6_detailed_1, merit6_detailed_2,
    safety_detailed_1, safety_detailed_2,
    summary_slide, ref_slide
]

save_json("output_manifest/20251215_copilot_sier_proposal_standard_content.json", {"slides": standard_slides})
save_json("output_manifest/20251215_copilot_sier_proposal_detailed_content.json", {"slides": detailed_slides})
