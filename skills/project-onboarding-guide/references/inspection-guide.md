# 检查指引

当仓库规模较大、结构含糊，或拆分成多个应用与服务时，使用这份参考说明。

## 证据优先级

1. 先读 `README*` 或其他根目录文档。
2. 再读根目录清单文件和任务执行文件。
3. 只针对真正相关的包去读 workspace 或子应用清单。
4. 只有在显式文档和脚本不够时，才读取源码入口文件。
5. 凡是根据源码结构推导出的内容，都标记为“推断”。

## 常见启动信号

### JavaScript 与 TypeScript

- 在查看源码前，先检查 `package.json` 里的 scripts。
- 检查 workspace 信号：`pnpm-workspace.yaml`、`turbo.json`、`nx.json`、`lerna.json`。
- 检查 `apps/`、`packages/`、`services/`、`libs/` 下的应用级清单文件。
- 检查框架配置文件，例如 `next.config.*`、`vite.config.*`、`nest-cli.json`、`astro.config.*`、`nuxt.config.*`。

### Python

- 检查 `pyproject.toml`、`requirements.txt`、`Pipfile`、`poetry.lock`、`uv.lock`、`Makefile`。
- 检查是否存在 `manage.py`、`main.py`、`app.py`、`wsgi.py`、`asgi.py`。
- 优先采用文档中声明的命令，而不是自行推断 `uvicorn` 或 `python -m` 入口。

### Go、Rust、Java 与其他语言

- 检查 `go.mod`、`Cargo.toml`、`pom.xml`、`build.gradle*`、`gradlew`。
- 检查常见入口位置，例如 `cmd/*`、`src/main.rs`、`src/main/`。
- 除非仓库里明确声明，否则对命令保持保守表述。

### 容器与基础设施

- 检查 `docker-compose.*`、`compose.*`、`Dockerfile*`、`.devcontainer/` 和部署清单。
- 除非文档明确将其定义为默认方式，否则把容器编排视为备选运行路径。

## 目录梳理启发式

- 当这些目录存在时，优先解释 `apps/`、`packages/`、`services/`、`src/`、`docs/`、`scripts/`、`config/`、`infra/`、`public/`、`migrations/`、`tests/`。
- 对 `dist/`、`build/`、`coverage/`、`.next/`、`target/`、`node_modules/` 这类生成目录，除非用户特别关注，否则应跳过或弱化描述。
- 给目录定性时要以内容为依据，不要只信目录名。

## 输出要求

- 保持概览简短且具体。
- 目录说明应聚焦在新协作者最需要先理解的少数目录。
- 将显式命令和推断命令区分开。
- 当仓库文档不足时，以缺失信息或待确认问题结尾。
