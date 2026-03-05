# 要求：检查 "abc12345" 密码的强，必须：
pwd_str = "abc12345"

# 长度不小于8位
cond1 = len(pwd_str) >= 8
# 必须包含数字
cond2 = any(c.isdigit() for c in pwd_str)
# 必须包含字母
cond3 = any(c.isalpha() for c in pwd_str)

# 满足条件
if cond1 and cond2 and cond3:
    print("密码强度高")
else:
    print("密码强度低")
