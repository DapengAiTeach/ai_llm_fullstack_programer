# 把用户名 "  aLiCe123  " 去掉空格，首字母大写，其余小写
name = "  aLiCe123  "
name = name.strip().lower().title()
print(name)