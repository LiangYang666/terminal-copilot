#!/usr/bin/env python3

import requests
import argparse
import os
import platform
from colorama import Fore, Style, init
import json
import yaml


def get_linux_distro():
    """
    检查 /etc/os-release 文件，识别 Linux 发行版。
    """
    try:
        with open("/etc/os-release") as f:
            os_release_info = f.read().lower()
        if "centos" in os_release_info:
            return "centos"
        elif "ubuntu" in os_release_info:
            return "ubuntu"
        elif "fedora" in os_release_info:
            return "fedora"
        elif "debian" in os_release_info:
            return "debian"
        else:
            return "linux"  # 未知 Linux 发行版
    except FileNotFoundError:
        return "linux"  # 如果没有 /etc/os-release 文件，返回通用 Linux


def get_system_type():
    system_type = platform.system().lower()

    if "linux" in system_type:
        distro_name = get_linux_distro()
        if "centos" in distro_name:
            return "你是一个熟悉CentOS系统的终端助手。用户可能会向你询问如何在终端中执行一些命令或完成特定任务。请给出适用于CentOS的精确命令和步骤。注意一定要简洁，因为你存在于终端上。"
        elif "ubuntu" in distro_name:
            return "你是一个熟悉Ubuntu系统的终端助手。用户可能会向你询问如何在终端中执行一些命令或完成特定任务。请给出适用于Ubuntu的精确命令和步骤。"
        else:
            return f"你是一个熟悉{distro_name.capitalize()}系统的终端助手。用户可能会向你询问如何在终端中执行一些命令或完成特定任务。请给出适用于{distro_name.capitalize()}的精确命令和步骤。"
    elif "darwin" in system_type:
        return "你是一个熟悉macOS系统的终端助手。用户可能会向你询问如何在终端中执行一些命令或完成特定任务。请给出适用于macOS的精确命令和步骤。"
    elif "windows" in system_type:
        return "你是一个熟悉Windows系统的终端助手。用户可能会向你询问如何在命令行中执行一些命令或完成特定任务。请给出适用于Windows CMD或PowerShell的精确命令和步骤。"
    else:
        return "你是一个熟悉多平台系统的终端助手。用户可能会向你询问如何在终端中执行一些命令或完成特定任务。请给出适用于Linux、macOS或Windows的通用命令和步骤。"


def stream_chat(api_url, model, api_key, user_query):
    url = api_url
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    system_type = get_system_type()

    data = {
        "model": model,  # 替换成你要使用的模型
        "messages": [
            {
                "role": "system",
                "content": f"你是一个熟悉{system_type}系统的终端助手。用户可能会向你询问如何在终端中执行一些命令或完成特定任务。请给出适用于{system_type}的精确命令和步骤。注意一定要简洁，因为你存在于终端上"
            },
            {"role": "user", "content": user_query}
        ],
        "stream": True,
    }

    # 发起请求并流式处理响应
    response = requests.post(url, headers=headers, json=data, stream=True)
    if response.status_code != 200:
        print("Error:", response.json())
        return

    response.encoding = 'utf-8'

    in_code_block = False
    try:
        display_message = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                # 从响应中提取内容
                content = line.split('data: ')[-1].strip()
                if content == "[DONE]":
                    if len(display_message) > 0:
                        display_message, in_code_block = display(display_message, in_code_block)
                    break

                # 解析JSON并处理内容
                content_json = json.loads(content)
                message = content_json.get("choices", [{}])[0].get("delta", {}).get("content", "")


                display_message += message

                if display_message.endswith("`"):
                    continue

                display_message, in_code_block = display(display_message, in_code_block)

    except Exception as e:
        print("Error while streaming response:", str(e))


def display(message, in_code_block):
    if "```" in message:
        in_code_block = not in_code_block
        if in_code_block:
            message = message.replace("```", Fore.GREEN + "```")
        else:
            message = message.replace("```", Fore.GREEN + "```" + Style.RESET_ALL)
        print(message, end="")
    else:
        if in_code_block:
            print(Fore.GREEN + message, end="")
        else:
            print(message, end="")
    message = ""
    return message, in_code_block


def main():
    parser = argparse.ArgumentParser(description="Terminal Copilot")
    parser.add_argument("query", type=str, nargs='+', help="Query to ask the copilot")
    args = parser.parse_args()
    user_query = ' '.join(args.query)

    api_key = "sk-xxx"
    api_url = "https://api.openai.com/v1/chat/completions"
    model = "gpt-4o-mini-0718"

    # 读取yaml配置文件
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        if config:
            api_key = config.get("OPENAI_API_KEY", api_key)
            api_url = config.get("OPENAI_API_URL", api_url)
            model = config.get("OPENAI_API_MODEL", model)

    api_key = os.getenv("OPENAI_API_KEY", api_key)
    api_url = os.getenv("OPENAI_API_URL", api_url)
    model = os.getenv("OPENAI_API_MODEL", model)

    # 初始化 colorama
    init(autoreset=True)

    stream_chat(api_url=api_url,
                model=model,
                api_key=api_key,
                user_query=user_query)


if __name__ == "__main__":
    main()
