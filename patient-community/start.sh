#!/bin/bash

# 患者社区 - 前后端启动脚本
# 用法: ./start.sh 或在 Finder 中双击 start.command

set -e

# 获取脚本所在目录（即 patient-community 根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  患者社区 - 启动前后端服务"
echo "========================================"
echo ""
echo "项目目录: $SCRIPT_DIR"
echo ""

# 用于存储后台进程 PID
BACKEND_PID=""

# 退出时清理：杀死后端进程
cleanup() {
  echo ""
  echo "正在停止服务..."
  if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
    echo "后端服务已停止 (PID: $BACKEND_PID)"
  fi
  echo "所有服务已停止。"
  exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# 启动后端
echo ">>> 启动后端服务 (FastAPI - 端口 8000)..."
cd "$SCRIPT_DIR/backend"
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
  echo "提示: 未检测到虚拟环境，使用系统 Python"
fi
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd "$SCRIPT_DIR"

# 等待后端启动
sleep 2

# 启动前端
echo ">>> 启动前端服务 (Vite - 端口 3000)..."
cd "$SCRIPT_DIR/frontend"
if command -v pnpm &>/dev/null; then
  pnpm dev
else
  npm run dev
fi
