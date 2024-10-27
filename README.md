# terminal-copilot
终端助手


### 一、参数设置：
1. 直接设置环境变量
```bash
export OPENAI_API_URL="https://api.openai.com/v1/chat/completions"
export OPENAI_API_KEY="sk-xxx"
export OPENAI_API_MODEL="gpt-4o"
```
注意，设置环境变量只会该终端生效，可将这几条命令添加到~/.bashrc文件中
2. 设置配置
例如将如下配置写入 `~/.terminal-copilot.yaml` 中，案例为使用本地ollama
```bash
OPENAI_API_URL: "http://localhost:11434/v1/chat/completions"
OPENAI_API_KEY: "sk-xxx"
OPENAI_API_MODEL: "llama3.1:70b"
```

### 二、使用
#### 2.1 添加至环境变量
mkdir ~/.local/bin
cp copilot.py ~/.local/bin/copilot
#### 2.2 使用
执行如下
copilot find命令怎么使用


## 问题记录
如报错 ImportError: urllib3 v2 only supports OpenSSL 1.1.1+
可降级，pip3 install urllib3==1.26.6