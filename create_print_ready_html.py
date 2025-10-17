#!/usr/bin/env python3
"""
印刷用HTMLを生成（ブラウザの印刷機能でPDF化可能）
"""

import re

def create_print_css():
    """印刷用CSS"""
    return """
    <style>
        @media print {
            @page {
                size: A4;
                margin: 2cm;
            }
            body {
                font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic", "Meiryo", sans-serif;
                line-height: 1.6;
                color: #333;
            }
            h1 {
                font-size: 24pt;
                page-break-before: always;
                margin-top: 0;
            }
            h1:first-of-type {
                page-break-before: avoid;
            }
            h2 {
                font-size: 18pt;
                margin-top: 1.5em;
            }
            h3 {
                font-size: 14pt;
                margin-top: 1.2em;
            }
            img {
                max-width: 100%;
                page-break-inside: avoid;
            }
            pre, code {
                font-family: "Consolas", "Courier New", monospace;
                background: #f5f5f5;
                padding: 0.5em;
            }
            table {
                page-break-inside: avoid;
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        }

        @media screen {
            body {
                max-width: 800px;
                margin: 2em auto;
                padding: 0 1em;
                font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic", "Meiryo", sans-serif;
                line-height: 1.8;
            }
            img {
                max-width: 100%;
                height: auto;
            }
            code {
                background: #f5f5f5;
                padding: 2px 5px;
                border-radius: 3px;
            }
            pre {
                background: #f5f5f5;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
            }
        }
    </style>
    """

def main():
    html_file = "final/完成版_家庭でできる肉の発酵熟成.html"
    output_file = "final/完成版_家庭でできる肉の発酵熟成_印刷用.html"

    # HTMLファイルを読み込み
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # CSSを追加
    print_css = create_print_css()

    # </head>の直前にCSSを挿入
    html_content = html_content.replace('</head>', f'{print_css}\n</head>')

    # 印刷ボタンを追加
    print_button = '''
    <div style="text-align: center; margin: 2em 0; page-break-after: always;">
        <button onclick="window.print()" style="padding: 1em 2em; font-size: 16px; cursor: pointer;">
            📄 PDF として印刷
        </button>
        <p style="color: #666; margin-top: 1em;">
            このボタンをクリックして、ブラウザの印刷機能からPDFとして保存してください
        </p>
    </div>
    '''
    html_content = html_content.replace('<body>', f'<body>\n{print_button}')

    # 保存
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ 印刷用HTMLを生成しました: {output_file}")
    print("\n次のステップ:")
    print(f"1. ブラウザで {output_file} を開く")
    print("2. 「PDFとして印刷」ボタンをクリック、またはCmd+P（Mac）/ Ctrl+P（Windows）")
    print("3. 送信先を「PDFに保存」に設定")
    print("4. 保存")

if __name__ == "__main__":
    main()
