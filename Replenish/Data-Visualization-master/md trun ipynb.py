import nbformat

md_file = "Dash/1/Dash教學.md"   # ✅ 改為正確格式
ipynb_file = "Dash/1/Dash教學.ipynb"

with open(md_file, 'r', encoding='utf-8') as f:
    content = f.read()

nb = nbformat.v4.new_notebook()
nb.cells.append(nbformat.v4.new_markdown_cell(content))

with open(ipynb_file, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"✅ 已成功轉換為 {ipynb_file}")
