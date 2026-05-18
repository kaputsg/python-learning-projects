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
```

### V3 数据库版本

V3 在 V2 面向对象版本的基础上，将数据保存方式从 JSON 文件升级为 SQLite 数据库。

### 新增功能

- 使用 SQLite 数据库保存记账记录
- 程序启动时自动创建 records 表
- 添加收入记录
- 添加支出记录
- 查看所有记录
- 查看余额统计
- 根据 ID 删除记录
- 根据 ID 修改记录
- 按日期查询记录
- 按分类统计支出
- 按日期范围查询记录
- 按月份统计收入、支出和余额

### 使用到的技术

- sqlite3
- CREATE TABLE
- INSERT
- SELECT
- SUM
- DELETE
- UPDATE
- GROUP BY
- BETWEEN
- LIKE
- datetime
- pathlib
- 面向对象编程

### 文件说明

- `accounting_v1.py`：函数版本，使用 JSON 保存数据
- `accounting_v2.py`：面向对象版本，使用 JSON 保存数据
- `accounting_v3.py`：数据库版本，使用 SQLite 保存数据

### 本地数据文件

- `accounting.db` 是本地数据库文件
- `records.json` 是 V1 / V2 的本地数据文件

这两个文件包含本地数据，不上传到 GitHub。

### V4 模块化版本

V4 在 V3 SQLite 数据库版本的基础上，将项目从单文件结构升级为多文件模块化结构。

### V4 新增功能

- 使用 `main.py` 作为程序入口
- 使用 `database.py` 管理数据库连接和 SQL 执行
- 使用 `utils.py` 管理通用工具函数
- 使用 `accounting_system.py` 管理记账系统主逻辑
- 支持关键词搜索记录
- 支持按金额范围查询记录
- 支持导出 CSV 报表
- 支持备份 SQLite 数据库

### V4 文件说明

- `main.py`：程序入口
- `database.py`：数据库管理模块
- `utils.py`：工具函数模块
- `accounting_system.py`：主业务逻辑模块
- `accounting_v1.py`：V1 函数版本
- `accounting_v2.py`：V2 面向对象 JSON 版本
- `accounting_v3.py`：V3 SQLite 单文件版本

### 本地数据文件

以下文件或文件夹只用于本地运行，不上传到 GitHub：

- `accounting.db`
- `records.json`
- `accounting_report.csv`
- `backups/`

### V5 FastAPI 后端版本

V5 在 V4 模块化命令行版本的基础上，新增 FastAPI 后端接口，使记账系统可以通过 HTTP API 访问。

### V5 新增功能

- 使用 FastAPI 创建后端服务
- 使用 Uvicorn 运行 API 服务
- 支持自动生成接口文档 `/docs`
- 支持查看所有记录接口
- 支持添加记录接口
- 支持修改记录接口
- 支持删除记录接口
- 支持余额统计接口
- 支持按月份统计收支
- 支持按分类统计支出
- 支持关键词搜索记录
- 支持按日期查询记录
- 支持按日期范围查询记录
- 支持按金额范围查询记录
- 添加记录后返回新记录 ID

### V5 API 接口

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/` | 测试 API 是否运行 |
| GET | `/records` | 查看所有记录 |
| POST | `/records` | 添加记录 |
| PUT | `/records/{record_id}` | 修改指定 ID 的记录 |
| DELETE | `/records/{record_id}` | 删除指定 ID 的记录 |
| GET | `/summary` | 查看总收入、总支出和余额 |
| GET | `/summary/month` | 按月份统计收支 |
| GET | `/summary/expense-by-category` | 按分类统计支出 |
| GET | `/records/search` | 按关键词搜索记录 |
| GET | `/records/by-date` | 按日期查询记录 |
| GET | `/records/by-date-range` | 按日期范围查询记录 |
| GET | `/records/by-amount-range` | 按金额范围查询记录 |

### 运行 FastAPI 服务

先安装依赖：

```bash
pip install -r requirements.txt

### V6 前端页面版本

V6 在 V5 FastAPI 后端接口版本的基础上，新增前端页面，通过 HTML、CSS 和 JavaScript 调用后端 API，实现一个可视化的个人记账系统页面。

### V6 新增功能

- 新增 `frontend/index.html` 前端页面
- 使用 `fetch()` 调用 FastAPI 后端接口
- 页面自动加载总览统计
- 页面自动加载所有记账记录
- 支持在网页中添加收入和支出记录
- 支持在网页中修改记录
- 支持在网页中删除记录
- 支持关键词搜索记录
- 支持按日期范围筛选记录
- 支持按金额范围筛选记录
- 支持月度收支统计
- 支持分类支出统计
- 金额统一保留两位小数
- 页面采用简约科技风格设计

### V6 使用到的技术

- HTML
- CSS
- JavaScript
- fetch API
- DOM 操作
- FastAPI
- SQLite
- CORS
- 前后端分离基础思想

### V6 文件说明

- `api.py`：FastAPI 后端接口
- `database.py`：数据库管理模块
- `utils.py`：工具函数模块
- `accounting_system.py`：命令行业务逻辑模块
- `main.py`：命令行版本入口
- `frontend/index.html`：前端页面
- `requirements.txt`：项目依赖文件

### 运行方式

先启动后端服务：

```bash
uvicorn api:app --reload