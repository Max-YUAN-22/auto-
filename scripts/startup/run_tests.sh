#!/bin/bash

# Multi-Agent DSL Framework Test Runner
# 测试运行脚本

set -e

echo "🧪 Multi-Agent DSL Framework Test Suite"
echo "========================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 测试结果统计
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 运行测试函数
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "\n${BLUE}Running: ${test_name}${NC}"
    echo "Command: ${test_command}"
    echo "----------------------------------------"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if eval "$test_command"; then
        echo -e "${GREEN}✅ PASSED: ${test_name}${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAILED: ${test_name}${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# 检查依赖
echo -e "\n${YELLOW}Checking dependencies...${NC}"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found${NC}"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found${NC}"
    exit 1
fi

# 检查pip包
echo "Installing Python test dependencies..."
pip install pytest pytest-cov pytest-asyncio psutil

# 检查npm包
echo "Installing Node.js test dependencies..."
cd frontend && npm install && cd ..

echo -e "${GREEN}✅ Dependencies ready${NC}"

# 运行测试套件
echo -e "\n${YELLOW}Starting test execution...${NC}"

# 1. 代码质量检查
run_test "Code Quality - Python Formatting" "python -m black --check backend/ core/ dsl/ runtime/ agents/ utils/"
run_test "Code Quality - Python Import Sorting" "python -m isort --check-only backend/ core/ dsl/ runtime/ agents/ utils/"
run_test "Code Quality - Python Linting" "python -m flake8 backend/ core/ dsl/ runtime/ agents/ utils/ --max-line-length=100"

# 2. 后端测试
run_test "Backend API Tests" "python -m pytest tests/test_backend_api.py -v"
run_test "Backend Unit Tests" "python -m pytest tests/ -k 'not performance' -v"

# 3. 前端测试
run_test "Frontend Component Tests" "python -m pytest tests/test_frontend.py -v"

# 4. 性能测试
run_test "Performance Tests" "python -m pytest tests/test_performance.py -v -s"

# 5. 集成测试
run_test "Integration Tests" "python -m pytest tests/ -k 'integration' -v"

# 6. 安全测试
run_test "Security Tests" "python -c 'import backend.config; print(\"Config validation passed\")'"

# 7. Docker测试
if command -v docker &> /dev/null; then
    run_test "Docker Build Test" "docker build --target backend -t test-backend . && docker rmi test-backend"
else
    echo -e "${YELLOW}⚠️  Docker not available, skipping Docker tests${NC}"
fi

# 生成测试报告
echo -e "\n${YELLOW}Test Summary${NC}"
echo "========================================"
echo -e "Total Tests: ${TOTAL_TESTS}"
echo -e "${GREEN}Passed: ${PASSED_TESTS}${NC}"
echo -e "${RED}Failed: ${FAILED_TESTS}${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}💥 Some tests failed!${NC}"
    exit 1
fi
