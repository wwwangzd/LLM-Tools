# 输出模板（可按项目替换）

## 1 requirements.txt 模板

```txt
# Core runtime
flask
gunicorn

# CANN / NPU runtime base deps
attrs
cython
numpy>=1.19.2,<2.0
decorator
sympy
cffi
pyyaml
pathlib2
psutil
protobuf==3.20.0
scipy
requests
absl-py

# Model stack
# torch==<to-confirm>
# torch-npu installed separately in Dockerfile

# Add project-specific deps below
# pillow
# opencv-python-headless
```

## 2 Dockerfile 模板

```dockerfile
FROM swr.cn-south-1.myhuaweicloud.com/ascendhub/cann:8.2.rc1-310p-openeuler22.03-py3.11

LABEL description="<service-name>"

WORKDIR /usr/service

ENV TZ=Asia/Shanghai

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo 'Asia/Shanghai' > /etc/timezone

RUN yum install -y wget mesa-libGL && \
    yum clean all

# 安装 Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh

# 配置 conda-forge
RUN cat > /opt/conda/.condarc <<EOF
channels:
  - conda-forge
show_channel_urls: true
EOF

# 创建 python=3.9 环境（按项目实际版本替换）
RUN conda create -n py39 python=3.9 -y && \
    conda clean -a -y

ENV PATH=/opt/conda/envs/py39/bin:$PATH

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir torch-npu

# Optional project dirs
# RUN mkdir -p /usr/output_dir/logs

# Copy model and service files
# COPY checkpoints/ /usr/service/checkpoints/
# COPY app.py .
# COPY run.sh .

# RUN chmod +x run.sh

EXPOSE <service-port>

CMD ["./run.sh"]
```

## 3 生成时替换项
- `<service-name>`: 服务名称（来自运行命令或项目名称）。
- `<service-port>`: 实际对外端口（例如 8501）。
- conda Python 版本与环境名：按给出或推测环境替换。
- `COPY` 列表：严格按当前项目文件存在性填写。
- `CMD`：优先使用项目现有启动脚本。

## 4 最终输出附加说明模板
- 事实：列出来自文件内容的确定信息。
- 推断：列出依赖当前信息做出的建议配置。
- 未知：列出待用户确认的版本、入口、回调地址等。
