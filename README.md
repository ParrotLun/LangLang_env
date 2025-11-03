# Jupyter Lab AI 開發環境

基於 Jupyter Lab 的 AI 開發環境，整合 LangGraph、LangChain 等先進的大型語言模型開發工具。

## 📋 專案簡介

本專案提供了一個完整的 Docker 容器化開發環境，適合進行以下工作：

- 🤖 大型語言模型（LLM）應用開發
- 🔄 LangGraph 工作流程設計
- 📚 LangChain 鏈式呼叫開發
- 🚀 FastAPI 後端服務建置
- 📊 資料科學與機器學習實驗

## ✨ 功能特色

- **Jupyter Lab 環境**：提供互動式開發介面
- **LangGraph 整合**：支援複雜的 AI Agent 工作流程
- **LangChain 生態系**：完整的 LLM 開發工具鏈
- **資料庫支援**：PostgreSQL 連接與操作
- **API 開發**：FastAPI 與 Uvicorn 支援
- **無密碼登入**：開發環境快速啟動

## 🛠️ 環境需求

- Docker Engine 20.10 或更新版本
- Docker Compose（選用）
- 至少 4GB 可用記憶體
- 至少 2GB 可用磁碟空間

## 📦 安裝步驟

### 1. 準備專案檔案

建立專案目錄結構：

```bash
mkdir -p my-jupyter-project/data
cd my-jupyter-project
```

### 2. 建立 Dockerfile

建立 `Dockerfile` 檔案，內容如下：

```dockerfile
FROM quay.io/jupyter/minimal-notebook:2025-09-30

COPY requirements.txt /tmp/requirements.txt

USER root

RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    rm -rf /tmp/* && \
    echo "jovyan ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_USER

WORKDIR /mlsteam/lab

CMD ["sh", "-c", "start-notebook.py --port=${JUPYTER_PORT:-8888} --NotebookApp.token='' --NotebookApp.password=''"]
```

### 3. 建立 requirements.txt

建立 `requirements.txt` 檔案，內容如下：

```
langgraph
langgraph-checkpoint
langgraph-cli[inmem]
langgraph-supervisor
langmem
langchain
langchain-core
langchain-openai
langchain-community
langchain-postgres
openai
fastapi[standard]
uvicorn[standard]
pydantic
pydantic-settings
requests
httpx
python-dotenv
psycopg-binary
psycopg2-binary
pytest
pytest-asyncio
tenacity
loguru
python-docx
nbformat
```

### 4. 建置 Docker 映像檔

```bash
docker build -t my-jupyter-lab .
```

## 🚀 使用方式

### 啟動容器

```bash
docker run -it --rm -p 8888:8888 \
  -v "$(pwd)/data:/mlsteam/lab" \
  -u $(id -u):$(id -g) \
  --group-add users \
  my-jupyter-lab
```

### 參數說明

- `-it`：互動式終端模式
- `--rm`：容器停止後自動刪除
- `-p 8888:8888`：將容器的 8888 埠對應到本機的 8888 埠
- `-v "$(pwd)/data:/mlsteam/lab"`：掛載本地 data 目錄到容器內
- `-u $(id -u):$(id -g)`：使用當前使用者的 UID 和 GID
- `--group-add users`：將使用者加入 users 群組

### 存取 Jupyter Lab

容器啟動後，在瀏覽器中開啟：

```
http://localhost:8888
```

無需輸入密碼或 token 即可直接使用。

## 📚 已安裝套件說明

### LangGraph 相關
- **langgraph**：建構複雜的 AI Agent 工作流程
- **langgraph-checkpoint**：工作流程檢查點管理
- **langgraph-cli[inmem]**：命令列工具與記憶體內儲存
- **langgraph-supervisor**：多 Agent 協調管理
- **langmem**：記憶體管理工具

### LangChain 生態系
- **langchain**：核心框架
- **langchain-core**：核心功能模組
- **langchain-openai**：OpenAI 整合
- **langchain-community**：社群貢獻模組
- **langchain-postgres**：PostgreSQL 整合

### API 與後端
- **openai**：OpenAI 官方 SDK
- **fastapi[standard]**：現代化的 Web 框架
- **uvicorn[standard]**：ASGI 伺服器
- **pydantic**：資料驗證
- **pydantic-settings**：設定管理

### 工具與輔助
- **requests / httpx**：HTTP 客戶端
- **python-dotenv**：環境變數管理
- **psycopg-binary / psycopg2-binary**：PostgreSQL 驅動
- **pytest / pytest-asyncio**：測試框架
- **tenacity**：重試機制
- **loguru**：日誌記錄
- **python-docx**：Word 文件處理
- **nbformat**：Jupyter Notebook 格式處理

## 💡 使用範例

### 建立簡單的 LangChain 應用

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

# 設定 OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your-api-key"

# 初始化模型
llm = ChatOpenAI(model="gpt-4")

# 發送訊息
response = llm.invoke([HumanMessage(content="你好！")])
print(response.content)
```

### 建立 LangGraph 工作流程

```python
from langgraph.graph import Graph
from langchain_openai import ChatOpenAI

# 建立圖形工作流程
workflow = Graph()

# 添加節點和邊
# ... 你的工作流程邏輯

# 執行工作流程
result = workflow.invoke({"input": "your input"})
```

## ⚠️ 注意事項

1. **安全性**：此設定移除了 Jupyter Lab 的密碼保護，僅適用於本地開發環境，**請勿**在生產環境或公開網路中使用。

2. **檔案權限**：使用 `-u $(id -u):$(id -g)` 確保容器內建立的檔案與本地使用者權限一致。

3. **資料持久化**：所有在 `/mlsteam/lab` 目錄下的檔案都會同步到本地的 `./data` 目錄。

4. **API 金鑰**：使用 OpenAI 或其他服務時，請妥善保管 API 金鑰，建議使用 `.env` 檔案管理。

5. **記憶體需求**：某些大型模型可能需要更多記憶體，請根據需求調整 Docker 資源配置。

## 🔧 進階配置

### 自訂埠號

```bash
docker run -it --rm -p 9999:8888 \
  -v "$(pwd)/data:/mlsteam/lab" \
  -u $(id -u):$(id -g) \
  --group-add users \
  my-jupyter-lab
```

然後存取 `http://localhost:9999`

### 啟用密碼保護

修改 Dockerfile 中的 CMD 行，移除 `--NotebookApp.token='' --NotebookApp.password=''`

### 新增環境變數

```bash
docker run -it --rm -p 8888:8888 \
  -v "$(pwd)/data:/mlsteam/lab" \
  -e OPENAI_API_KEY="your-key" \
  -u $(id -u):$(id -g) \
  --group-add users \
  my-jupyter-lab
```

