from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
result = md.convert("D:\\Форматы данных ДГ tNavigator.xlsx")
print(result.text_content)