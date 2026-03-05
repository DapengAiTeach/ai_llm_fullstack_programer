# 将RGB元组转换为十六进制颜色代码
color1 = (255, 122, 185)
r, g, b = color1
color2 = f"#{r:02x}{g:02x}{b:02x}"
print(color2)

# 将十六进制颜色代码转换为RGB元组
color3 = tuple(int(color2[i:i + 2], 16) for i in (1, 3, 5))
print(color3)