# Personal Accounting System

这是一个使用 Python 编写的个人记账系统项目。

## 版本说明

### V1 函数版本

V1 主要实现了基础记账功能：

- 添加收入
- 添加支出
- 查看所有记录
- 查看余额统计
- 删除记录
- 修改记录
- 使用 JSON 文件保存数据
- 程序启动时自动读取历史记录

### V2 面向对象版本

V2 在 V1 的基础上进行了代码结构升级：

- 使用 `AccountingSystem` 类管理整个系统
- 使用 `self.records` 替代全局变量 `records`
- 将功能封装为类方法
- 合并添加收入和添加支出的重复代码
- 优化修改记录功能，支持直接回车保持原内容
- 封装记录编号输入逻辑
- 使用标准程序入口写法：

```python
if __name__ == "__main__":
    system = AccountingSystem()
    system.run()