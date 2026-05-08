# 基金趋势分析工具 V1
# 当前目标：实现菜单 + 输入基金数据功能


# 用来保存基金数据
fund_data = {
    "name": "",
    "prices": []
}


def show_menu():
    """显示主菜单"""
    print()
    print("========== 基金趋势分析工具 ==========")
    print("1. 查看项目说明")
    print("2. 输入基金数据")
    print("3. 分析基金涨跌")
    print("4. 分析基金风险")
    print("5. 生成完整报告")
    print("6. 保存完整报告到 txt 文件")
    print("0. 退出程序")
    print("====================================")


def show_project_info():
    """查看项目说明"""
    print()
    print("【项目说明】")
    print("本工具用于分析基金的涨跌趋势和风险等级。")
    print("当前版本为 V1，暂时需要用户手动输入基金数据。")
    print("后续版本可以升级为自动获取数据、生成日报、可视化图表等功能。")


def is_positive_number(text):
    """判断用户输入的内容是否是正数"""

    # 去掉前后空格
    text = text.strip()

    # 空内容不是数字
    if text == "":
        return False

    # 小数点不能超过 1 个
    if text.count(".") > 1:
        return False

    # 去掉一个小数点后，剩下的必须全是数字
    check_text = text.replace(".", "", 1)

    if check_text.isdigit():
        number = float(text)

        if number > 0:
            return True
        else:
            return False
    else:
        return False


def input_fund_data():
    """输入基金数据"""
    print()
    print("【输入基金数据】")

    name = input("请输入基金名称：").strip()

    if name == "":
        print("基金名称不能为空。")
        return

    prices = []

    print()
    print("请依次输入每天的基金净值。")
    print("输入 q 表示结束输入。")
    print("例如：1.000、1.012、0.998")

    day = 1

    while True:
        price_text = input(f"请输入第 {day} 天净值：").strip()

        if price_text == "q" or price_text == "Q":
            break

        if is_positive_number(price_text):
            price = float(price_text)
            prices.append(price)
            day += 1
        else:
            print("输入错误，请输入大于 0 的数字，或者输入 q 结束。")

    if len(prices) < 2:
        print()
        print("净值数据太少，至少需要输入 2 天数据。")
        print("本次数据不会保存。")
        return

    fund_data["name"] = name
    fund_data["prices"] = prices

    print()
    print("基金数据已保存。")
    print(f"基金名称：{fund_data['name']}")
    print(f"净值数据：{fund_data['prices']}")

def calculate_total_return(prices):
    """计算总涨跌幅"""
    first_price = prices[0]
    last_price = prices[-1]

    total_return = (last_price - first_price) / first_price * 100
    return total_return


def calculate_latest_change(prices):
    """计算最近一天涨跌幅"""
    yesterday_price = prices[-2]
    today_price = prices[-1]

    latest_change = (today_price - yesterday_price) / yesterday_price * 100
    return latest_change


def calculate_daily_changes(prices):
    """计算每日涨跌幅"""
    daily_changes = []

    for i in range(1, len(prices)):
        yesterday_price = prices[i - 1]
        today_price = prices[i]

        change = (today_price - yesterday_price) / yesterday_price * 100
        daily_changes.append(change)

    return daily_changes


def judge_trend(total_return, latest_change):
    """根据总涨跌幅和最近一天涨跌幅判断趋势"""

    if total_return > 3 and latest_change > 0:
        return "上涨趋势"

    elif total_return > 0 and latest_change < 0:
        return "震荡上涨"

    elif total_return < -3 and latest_change < 0:
        return "下跌趋势"

    elif total_return < 0 and latest_change > 0:
        return "震荡下跌"

    else:
        return "横盘震荡"

def analyze_fund_change():
    """分析基金涨跌"""
    print()
    print("【分析基金涨跌】")

    if fund_data["name"] == "" or len(fund_data["prices"]) < 2:
        print("你还没有输入有效的基金数据，请先选择 2 输入基金数据。")
        return

    name = fund_data["name"]
    prices = fund_data["prices"]

    first_price = prices[0]
    last_price = prices[-1]

    total_return = calculate_total_return(prices)
    latest_change = calculate_latest_change(prices)
    daily_changes = calculate_daily_changes(prices)

    trend = judge_trend(total_return, latest_change)

    print(f"基金名称：{name}")
    print(f"起始净值：{first_price}")
    print(f"最新净值：{last_price}")
    print(f"总涨跌幅：{total_return:.2f}%")
    print(f"最近一天涨跌幅：{latest_change:.2f}%")

    print("每日涨跌幅：")
    for i in range(len(daily_changes)):
        print(f"第 {i + 1} 天到第 {i + 2} 天：{daily_changes[i]:.2f}%")

    print(f"趋势判断：{trend}")

def calculate_max_drawdown(prices):
    """计算最大回撤"""
    highest_price = prices[0]
    max_drawdown = 0

    for price in prices:
        if price > highest_price:
            highest_price = price

        drawdown = (highest_price - price) / highest_price * 100

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return max_drawdown


def calculate_average_volatility(daily_changes):
    """计算平均波动幅度"""
    total = 0

    for change in daily_changes:
        total += abs(change)

    average_volatility = total / len(daily_changes)
    return average_volatility


def count_consecutive_down_days(prices):
    """计算最近连续下跌天数"""
    count = 0

    for i in range(len(prices) - 1, 0, -1):
        if prices[i] < prices[i - 1]:
            count += 1
        else:
            break

    return count


def calculate_risk_score(max_drawdown, average_volatility, consecutive_down_days, latest_change):
    """根据多个风险指标计算风险分数"""
    score = 0

    # 1. 最大回撤风险
    if max_drawdown >= 10:
        score += 3
    elif max_drawdown >= 5:
        score += 2
    elif max_drawdown >= 2:
        score += 1

    # 2. 平均波动风险
    if average_volatility >= 2:
        score += 2
    elif average_volatility >= 1:
        score += 1

    # 3. 连续下跌风险
    if consecutive_down_days >= 3:
        score += 2
    elif consecutive_down_days >= 2:
        score += 1

    # 4. 最近一天大跌风险
    if latest_change <= -3:
        score += 2
    elif latest_change <= -1:
        score += 1

    return score


def judge_risk_level(score):
    """根据风险分数判断风险等级"""
    if score >= 6:
        return "高风险"
    elif score >= 3:
        return "中等风险"
    else:
        return "低风险"


def analyze_fund_risk():
    """分析基金风险"""
    print()
    print("【分析基金风险】")

    if fund_data["name"] == "" or len(fund_data["prices"]) < 2:
        print("你还没有输入有效的基金数据，请先选择 2 输入基金数据。")
        return

    name = fund_data["name"]
    prices = fund_data["prices"]

    daily_changes = calculate_daily_changes(prices)
    latest_change = calculate_latest_change(prices)

    max_drawdown = calculate_max_drawdown(prices)
    average_volatility = calculate_average_volatility(daily_changes)
    consecutive_down_days = count_consecutive_down_days(prices)

    risk_score = calculate_risk_score(
        max_drawdown,
        average_volatility,
        consecutive_down_days,
        latest_change
    )

    risk_level = judge_risk_level(risk_score)

    print(f"基金名称：{name}")
    print(f"最大回撤：{max_drawdown:.2f}%")
    print(f"平均波动幅度：{average_volatility:.2f}%")
    print(f"连续下跌天数：{consecutive_down_days}天")
    print(f"最近一天涨跌幅：{latest_change:.2f}%")
    print(f"风险分数：{risk_score}")
    print(f"风险等级：{risk_level}")

    if risk_level == "高风险":
        print("风险提示：近期风险较高，不建议盲目操作，应先观察。")
    elif risk_level == "中等风险":
        print("风险提示：基金存在一定波动，需要注意追高或连续下跌风险。")
    else:
        print("风险提示：当前风险不高，但仍需要继续观察。")

def generate_advice(trend, risk_level):
    """根据趋势和风险等级生成综合提示"""

    if risk_level == "高风险":
        return "近期风险较高，不建议盲目操作，应先观察走势变化。"

    elif risk_level == "中等风险":
        if trend == "上涨趋势":
            return "基金整体表现较好，但存在一定波动，不建议一次性重仓。"
        elif trend == "震荡上涨":
            return "基金整体上涨，但短期有回落，需要注意追高风险。"
        elif trend == "下跌趋势":
            return "基金处于下跌趋势，同时存在一定风险，需要谨慎观察。"
        else:
            return "基金走势不够稳定，存在一定波动，建议继续观察。"

    else:
        if trend == "上涨趋势":
            return "基金趋势相对较好，当前风险较低，但仍需要持续跟踪。"
        elif trend == "震荡上涨":
            return "基金整体略有上涨，当前风险不高，但短期波动需要关注。"
        elif trend == "震荡下跌":
            return "当前风险不高，但基金整体表现偏弱，可以继续观察。"
        else:
            return "当前风险不高，但趋势还不够明显，可以继续观察。"
        
def create_report_text():
    """创建完整基金分析报告文本"""

    if fund_data["name"] == "" or len(fund_data["prices"]) < 2:
        return None

    name = fund_data["name"]
    prices = fund_data["prices"]

    first_price = prices[0]
    last_price = prices[-1]

    # 涨跌分析
    total_return = calculate_total_return(prices)
    latest_change = calculate_latest_change(prices)
    daily_changes = calculate_daily_changes(prices)
    trend = judge_trend(total_return, latest_change)

    # 风险分析
    max_drawdown = calculate_max_drawdown(prices)
    average_volatility = calculate_average_volatility(daily_changes)
    consecutive_down_days = count_consecutive_down_days(prices)

    risk_score = calculate_risk_score(
        max_drawdown,
        average_volatility,
        consecutive_down_days,
        latest_change
    )

    risk_level = judge_risk_level(risk_score)

    # 综合提示
    advice = generate_advice(trend, risk_level)

    report_text = f"""
========== 基金完整分析报告 ==========
基金名称：{name}
起始净值：{first_price}
最新净值：{last_price}

【涨跌分析】
总涨跌幅：{total_return:.2f}%
最近一天涨跌幅：{latest_change:.2f}%
趋势判断：{trend}

【风险分析】
最大回撤：{max_drawdown:.2f}%
平均波动幅度：{average_volatility:.2f}%
连续下跌天数：{consecutive_down_days}天
风险分数：{risk_score}
风险等级：{risk_level}

【综合提示】
{advice}
====================================
"""

    return report_text

def generate_report():
    """生成完整基金分析报告"""
    print()
    print("【生成完整报告】")

    report_text = create_report_text()

    if report_text is None:
        print("你还没有输入有效的基金数据，请先选择 2 输入基金数据。")
        return

    print(report_text)

def save_report_to_txt():
    """把完整报告保存到 txt 文件"""
    print()
    print("【保存报告到 txt 文件】")

    report_text = create_report_text()

    if report_text is None:
        print("你还没有输入有效的基金数据，请先选择 2 输入基金数据。")
        return

    filename = "fund_report.txt"

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report_text)

        print(f"报告已保存到：{filename}")

    except:
        print("保存失败，请检查文件是否被占用，或者当前文件夹是否有写入权限。")


def main():
    """主程序入口"""
    while True:
        show_menu()
        choice = input("请输入你的选择：").strip()

        if choice == "1":
            show_project_info()

        elif choice == "2":
            input_fund_data()

        elif choice == "3":
            analyze_fund_change()

        elif choice == "4":
            analyze_fund_risk()

        elif choice == "5":
            generate_report()

        elif choice == "6":
            save_report_to_txt()

        elif choice == "0":
            print()
            print("程序已退出，感谢使用。")
            break

        else:
            print()
            print("输入错误，请输入 0-6 之间的数字。")


main()