import copy


def add_item(cart, name, price, quantity=1):
    """
    添加商品到购物车，如果已存在则累加数量
    :param cart: 购物车列表
    :param name: 名称
    :param price: 价格
    :param quantity: 数量
    :return: 新的购物车列表
    """
    inner_cart = copy.deepcopy(cart)
    for item in inner_cart:
        if item["name"] == name:
            # 已存在，数量增加
            item["quantity"] += quantity
        else:
            # 不存在，添加
            item = {"name": name, "price": price, "quantity": quantity}
            inner_cart.append(item)
    return inner_cart


def remove_item(cart, name):
    """从购物车移除商品"""
    inner_cart = copy.deepcopy(cart)
    for item in inner_cart:
        if item["name"] == name:
            # 找到，移除
            inner_cart.remove(item)
            break
    return inner_cart


def update_quantity(cart, name, quantity):
    """修改商品数量"""
    inner_cart = copy.deepcopy(cart)
    for item in inner_cart:
        if item["name"] == name:
            item["quantity"] = quantity
            break
    return inner_cart


def calculate_total(cart, discount_func=None):
    """计算总价，支持传入折扣函数"""
    total = 0.0
    # 计算原本的价格
    for item in cart:
        total += item["price"] * item["quantity"]
    # 计算折扣以后的价格
    if discount_func:
        total = discount_func(total)
    return total


def vip_discount(total):
    """vip 9折"""
    return total * 0.9


def holiday_discount(total):
    """满100减20"""
    if total >= 100:
        return total - 20
    else:
        return total


if __name__ == '__main__':
    # 购物车数据
    data = [{"name": "键盘", "price": 20, "quantity": 3}]

    # 添加商品
    data = add_item(data, "鼠标", 10, 5)

    # 修改数量
    data = update_quantity(data, "鼠标", 8)

    # 移除商品
    data = remove_item(data, "键盘")

    # 算总价
    total = calculate_total(data, vip_discount)
    print("总价：", total)
