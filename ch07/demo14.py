# "/home/user/documents/report.pdf" 提取文件名（不含路径）和扩展名，得到 report
file_path = "/home/user/documents/report.pdf"
file_name = file_path.split('/')[-1].split('.')[0]
print(file_name)