# Lambda MCP 快速开始指南

## 激活虚拟环境

项目使用虚拟环境来管理依赖。在运行任何命令之前，请先激活虚拟环境：

```bash
# 方法 1: 使用 source 激活（推荐用于交互式 shell）
source .venv/bin/activate

# 方法 2: 直接使用虚拟环境中的 Python
.venv/bin/python your_script.py
```

## 运行服务器

激活虚拟环境后：

```bash
python lambda_mcp.py
```

或者不激活虚拟环境，直接使用：

```bash
.venv/bin/python lambda_mcp.py
```

## 测试安装

运行测试脚本验证所有功能正常：

```bash
.venv/bin/python test_tools.py
```

## 工具使用示例

### 1. 查询 Data Explorer

```python
# 通过 MCP 调用
result = query_data_explorer(
    secret="your_secret_key",
    module_name="your_module",
    base_url="https://data-service.example.com",
    api_path="api/v1/service/query",
    dbname="your_database",
    sql="SELECT * FROM users LIMIT 10"
)
```

### 2. 查询 Elasticsearch

```python
# 通过 MCP 调用
result = query_elasticsearch_via_kibana(
    base_url="https://kibana.example.com",
    username="your_username",
    password="your_password",
    path="_cat/indices",
    jq_query=".[] | select(.index | contains(\"myindex\"))",
    query="{}"
)
```

## 环境变量

可以通过环境变量配置：

```bash
# 设置最大 token 数（默认 30000）
export LAMBDA_MCP_MAX_TOKEN_NUM=50000

# 然后运行服务器
.venv/bin/python lambda_mcp.py
```

## 开发模式

如果需要修改代码：

```bash
# 激活虚拟环境
source .venv/bin/activate

# 编辑代码...

# 测试修改
python test_tools.py

# 运行服务器
python lambda_mcp.py
```

## 目录结构

```
lambda-mcp/
├── lambda_mcp.py              # 主入口文件
├── lib/                       # 库文件
│   ├── data_explorer_client.py   # DataExplorer 客户端
│   └── response_utils.py         # 响应处理工具
├── tools/                     # MCP 工具
│   ├── data_explorer.py       # Data Explorer 工具
│   └── elasticsearch.py       # Elasticsearch 工具
└── test_tools.py              # 测试脚本
```

详细的架构说明请参考 [STRUCTURE.md](STRUCTURE.md)。

## 常见问题

### Q: 为什么需要激活虚拟环境？

A: 虚拟环境隔离了项目依赖，避免与系统 Python 包冲突。

### Q: 如果忘记激活虚拟环境怎么办？

A: 可以直接使用 `.venv/bin/python` 运行脚本，不需要激活。

### Q: 响应太大怎么办？

A: 工具会自动检测响应大小。如果超过 token 限制，会将结果保存到临时文件并返回文件路径。

### Q: 如何添加新工具？

A: 参考 [STRUCTURE.md](STRUCTURE.md) 中的"Adding New Tools"部分。
