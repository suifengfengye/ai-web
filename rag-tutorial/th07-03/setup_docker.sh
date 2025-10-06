# Git安装和项目克隆 start ----------------------------------------------------------
echo "Step 0 ============================================================================="
echo "Checking Git installation and cloning RAGFlow project..."

# Check if Git is already installed
if command -v git &> /dev/null; then
    echo "Git is already installed!"
    echo "Current version:"
    git --version
else
    echo "Installing Git..."
    
    # 更新系统包索引
    echo "Updating package index..."
    sudo apt-get update
    
    # 安装Git
    echo "Installing Git..."
    sudo apt-get install -y git
    
    # 验证Git安装
    if command -v git &> /dev/null; then
        echo "Git installed successfully!"
        git --version
    else
        echo "Failed to install Git"
        exit 1
    fi
fi

# Check if ragflow directory already exists
if [ -d "ragflow" ]; then
    echo "RAGFlow directory already exists, entering existing directory..."
    cd ragflow
    
    # 检查是否是有效的git仓库
    if [ -d ".git" ]; then
        echo "Existing RAGFlow repository found."
        echo "Current repository status:"
        git status --porcelain
        
        # 可选：更新代码（如果需要的话）
        echo "Pulling latest changes..."
        git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || echo "Failed to pull updates, continuing with existing code..."
    else
        echo "Warning: ragflow directory exists but is not a git repository."
        echo "Continuing with existing directory..."
    fi
else
    echo "Cloning RAGFlow project..."
    
    # 克隆项目（使用gitee镜像，国内访问更快）
    if git clone https://gitee.com/infiniflow/ragflow.git; then
        echo "RAGFlow project cloned successfully!"
        cd ragflow
    else
        echo "Failed to clone from gitee, trying GitHub..."
        if git clone https://github.com/infiniflow/ragflow.git; then
            echo "RAGFlow project cloned successfully from GitHub!"
            cd ragflow
        else
            echo "ERROR: Failed to clone RAGFlow project from both gitee and GitHub"
            echo "Please check your network connection and try again."
            exit 1
        fi
    fi
fi

echo "Current directory: $(pwd)"
echo "RAGFlow project setup completed!"
# Git安装和项目克隆 end -------------------------------------------------------------

# Docker安装和启动 start ----------------------------------------------------------
echo "Step 1 ============================================================================="
echo "Checking Docker installation..."

# Check if Docker is already installed
if command -v docker &> /dev/null; then
    echo "Docker is already installed!"
    echo "Current version:"
    docker --version
    
    # Check if Docker service is running
    if sudo systemctl is-active --quiet docker; then
        echo "Docker service is already running."
    else
        echo "Starting Docker service..."
        sudo systemctl start docker
        sudo systemctl enable docker
    fi
else
    echo "Installing Docker..."
    
    # 更新系统包索引
    echo "Updating package index..."
    sudo apt-get update
    
    # 安装必要的依赖（ca-certificates用于HTTPS，curl用于下载，gnupg用于密钥验证）
    echo "Installing required dependencies..."
    sudo apt-get install -y ca-certificates curl gnupg lsb-release
    
    # 创建密钥存储目录
    echo "Setting up Docker repository..."
    sudo mkdir -p /etc/apt/keyrings
    
    # 下载并添加阿里云Docker GPG密钥（国内加速）
    curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # 配置阿里云Docker源（适配Ubuntu 24.04 "noble"版本）
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu noble stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # 再次更新包索引（使新配置的源生效）
    echo "Updating package index with Docker repository..."
    sudo apt-get update
    
    # 安装Docker核心组件（ce为社区版，包含cli、容器运行时等）
    echo "Installing Docker components..."
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # 启动Docker服务
    echo "Starting Docker service..."
    sudo systemctl start docker
    
    # 设置Docker开机自启
    sudo systemctl enable docker
    
    # 检查Docker服务状态（应显示active (running)）
    echo "Checking Docker service status..."
    sudo systemctl status docker --no-pager
    
    # 创建Docker配置目录
    echo "Configuring Docker registry mirrors..."
    sudo mkdir -p /etc/docker
    
    # 配置阿里云镜像加速器
    sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://docker.1ms.run"]
}
EOF
    
    # 重启Docker使配置生效
    echo "Restarting Docker to apply configuration..."
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    
    # 验证Docker安装
    echo "Verifying Docker installation..."
    if command -v docker &> /dev/null && sudo systemctl is-active --quiet docker; then
        docker --version
        echo "Docker installed and started successfully!"
    else
        echo "Failed to install or start Docker"
        exit 1
    fi
fi

# 启动Docker Compose服务
echo "Starting RAGFlow services with Docker Compose..."
if [ -f "docker/docker-compose-base.yml" ]; then
    # 启动docker compose并捕获异常
    if docker compose -f docker/docker-compose-base.yml up -d; then
        echo "Docker Compose services started successfully!"
        
        # 检查容器状态
        echo "Checking container status..."
        sleep 5  # 等待容器启动
        
        # 获取启动的容器列表
        CONTAINERS=$(docker compose -f docker/docker-compose-base.yml ps --services)
        FAILED_CONTAINERS=""
        
        # 检查每个容器的状态
        for container in $CONTAINERS; do
            if ! docker compose -f docker/docker-compose-base.yml ps --status running | grep -q "$container"; then
                FAILED_CONTAINERS="$FAILED_CONTAINERS $container"
            fi
        done
        
        if [ -n "$FAILED_CONTAINERS" ]; then
            echo "ERROR: The following containers failed to start properly:$FAILED_CONTAINERS"
            echo "Container logs:"
            for container in $FAILED_CONTAINERS; do
                echo "=== Logs for $container ==="
                docker compose -f docker/docker-compose-base.yml logs "$container" --tail=20
            done
            echo "Stopping all containers due to startup failures..."
            docker compose -f docker/docker-compose-base.yml down
            exit 1
        else
            echo "All containers are running successfully!"
            echo "RAGFlow services are now available."
            docker compose -f docker/docker-compose-base.yml ps
        fi
    else
        echo "ERROR: Failed to start Docker Compose services"
        echo "Please check the docker-compose-base.yml file and try again."
        exit 1
    fi
else
    echo "ERROR: docker/docker-compose-base.yml file not found!"
    echo "Please make sure you are running this script from the RAGFlow root directory."
    exit 1
fi

# 1. Docker安装和启动 end -------------------------------------------------------------
