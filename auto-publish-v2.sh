#!/bin/bash

# AI Toolkit v0.3.0 自动化发布脚本
# 支持多平台自动发布

set -e

echo "🚀 AI Toolkit v0.3.0 自动化发布"
echo "================================"

# 配置
GITHUB_REPO="https://github.com/flowerjunjie/ai-toolkit"
PROJECT_NAME="AI Toolkit"
VERSION="v0.3.0"

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查工具
check_tool() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 已安装"
        return 0
    else
        echo -e "${YELLOW}✗${NC} $1 未安装"
        return 1
    fi
}

# Hacker News发布
publish_hackernews() {
    echo -e "\n${BLUE}[Hacker News]${NC} 发布中..."
    
    # 方法1: 使用Hacker News API（需要API key）
    if [ -n "$HACKERNEWS_API_KEY" ]; then
        curl -X POST "https://hacker-news.firebaseio.com/v0/item" \
            -H "Content-Type: application/json" \
            -d '{
                "title": "Show HN: AI Toolkit – 本地AI工具箱，790+命令，让AI开发更简单",
                "url": "'$GITHUB_REPO'",
                "text": "AI Toolkit是一个强大的本地AI模型管理和开发工具，让AI开发更简单。"
            }'
    else
        echo -e "${YELLOW}未设置HACKERNEWS_API_KEY${NC}"
        echo "请手动发布: https://news.ycombinator.com/submit"
    fi
}

# Reddit发布
publish_reddit() {
    echo -e "\n${BLUE}[Reddit]${NC} 发布中..."
    
    if [ -n "$REDDIT_CLIENT_ID" ] && [ -n "$REDDIT_CLIENT_SECRET" ] && [ -n "$REDDIT_USERNAME" ] && [ -n "$REDDIT_PASSWORD" ]; then
        # 获取access token
        ACCESS_TOKEN=$(curl -X POST -u "REDDIT_CLIENT_ID:REDDIT_CLIENT_SECRET" \
            -d "grant_type=password&username=REDDIT_USERNAME&password=REDDIT_PASSWORD" \
            "https://www.reddit.com/api/v1/access_token" | jq -r '.access_token')
        
        # 发布到r/MachineLearning
        curl -X POST "https://oauth.reddit.com/api/submit" \
            -H "Authorization: bearer $ACCESS_TOKEN" \
            -H "User-Agent: AI-Toolkit/1.0" \
            -d "api_type=json" \
            -d "sr=MachineLearning" \
            -d "title=[D] AI Toolkit - 本地AI工具箱，790+命令，企业级功能，开源免费" \
            -d "url=$GITHUB_REPO"
    else
        echo -e "${YELLOW}未设置Reddit API凭证${NC}"
        echo "请手动发布: https://www.reddit.com/r/MachineLearning/submit"
    fi
}

# Twitter发布
publish_twitter() {
    echo -e "\n${BLUE}[Twitter]${NC} 发布中..."
    
    if [ -n "$TWITTER_API_KEY" ] && [ -n "$TWITTER_API_SECRET" ] && [ -n "$TWITTER_ACCESS_TOKEN" ] && [ -n "$TWITTER_ACCESS_SECRET" ]; then
        # 使用Twitter API v2
        curl -X POST "https://api.twitter.com/2/tweets" \
            -H "Authorization: Bearer $TWITTER_BEARER_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{
                "text": "🚀 刚发布：AI Toolkit v0.3.0\n\n本地AI工具箱，790+命令，让AI开发更简单\n\n✅ 76个功能模块\n✅ 20+AI模型支持\n✅ 企业级功能（SSO、多租户）\n✅ GDPR/SOC2合规\n\nGitHub: https://github.com/flowerjunjie/ai-toolkit\n\n#AI #MachineLearning #OpenSource"
            }'
    else
        echo -e "${YELLOW}未设置Twitter API凭证${NC}"
        echo "请手动发布或使用第三方工具"
    fi
}

# LinkedIn发布
publish_linkedin() {
    echo -e "\n${BLUE}[LinkedIn]${NC} 发布中..."
    echo "LinkedIn需要手动发布"
    echo "请访问: https://www.linkedin.com/feed"
    echo "参考RELEASE_GUIDE_v0.3.0.md中的内容"
}

# V2EX发布
publish_v2ex() {
    echo -e "\n${BLUE}[V2EX]${NC} 发布中..."
    echo "V2EX需要手动发布（需要账号）"
    echo "请访问: https://www.v2ex.com/go/new"
    echo "参考RELEASE_GUIDE_v0.3.0.md中的内容"
}

# 检查可用的自动发布工具
check_auto_tools() {
    echo -e "\n${BLUE}检查自动发布工具...${NC}"
    
    # 检查常见工具
    tools=(
        "twurl" # Twitter CLI
        "rtv" # Reddit Terminal Viewer
        "t" # Twitter CLI
    )
    
    for tool in "${tools[@]}"; do
        check_tool $tool
    done
}

# 使用第三方服务
use_third_party_service() {
    echo -e "\n${BLUE}第三方自动发布服务${NC}"
    echo "推荐工具："
    echo ""
    echo "1. Buffer - https://buffer.com"
    echo "   - 支持多平台"
    echo "   - 定时发布"
    echo "   - 免费计划可用"
    echo ""
    echo "2. Hootsuite - https://hootsuite.com"
    echo "   - 企业级"
    echo "   - 多平台管理"
    echo "   - 免费计划可用"
    echo ""
    echo "3. Zapier - https://zapier.com"
    echo "   - 自动化工作流"
    echo "   - GitHub -> 社交媒体"
    echo "   - 免费计划可用"
    echo ""
    echo "4. IFTTT - https://ifttt.com"
    echo "   - 简单自动化"
    echo "   - GitHub -> 社交媒体"
    echo "   - 完全免费"
    echo ""
    echo "5. CrowdTangle - https://www.crowdtangle.com"
    echo "   - Facebook/Meta官方"
    echo "   - 免费使用"
    echo ""
    echo "6. Typefully - https://typefully.com"
    echo "   - Twitter专用"
    echo "   - 定时发布"
    echo "   - 免费计划"
    echo ""
    echo "7. Later - https://later.com"
    echo "   - 视觉化日历"
    echo "   - 多平台支持"
    echo "   - 免费计划"
}

# 使用GitHub Actions自动化
setup_github_actions() {
    echo -e "\n${BLUE}GitHub Actions自动化${NC}"
    echo "创建GitHub Actions工作流..."
    
    mkdir -p .github/workflows
    
    cat > .github/workflows/auto-social.yml << 'EOM'
name: Auto Social Post

on:
  release:
    types: [published]

jobs:
  post-to-social:
    runs-on: ubuntu-latest
    steps:
      - name: Post to Twitter
        uses: Eomm/social-post-action@v1
        with:
          webhook: ${{ secrets.TWITTER_WEBHOOK }}
          message: |
            🚀 New Release: ${{ github.event.release.tag_name }}
            
            ${{ github.event.release.name }}
            
            ${{ github.event.release.html_url }}
            
            #AI #MachineLearning #OpenSource
      
      - name: Post to Slack
        uses: slackapi/slack-github-action@v1.24.0
        with:
          payload: |
            {
              "text": "🚀 New Release: ${{ github.event.release.tag_name }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*${{ github.event.release.name }}*\n${{ github.event.release.html_url }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
EOM
    
    echo "✓ GitHub Actions工作流已创建"
    echo "请配置secrets: TWITTER_WEBHOOK, SLACK_WEBHOOK_URL"
}

# 主函数
main() {
    echo "请选择发布方式："
    echo "1) 手动发布（推荐，最可靠）"
    echo "2) API自动发布（需要配置API key）"
    echo "3) 第三方服务（Buffer, Hootsuite等）"
    echo "4) GitHub Actions自动化"
    echo "5) 查看所有选项"
    
    read -p "请选择 [1-5]: " choice
    
    case $choice in
        1)
            echo -e "\n${GREEN}手动发布指南${NC}"
            echo "请参考 RELEASE_GUIDE_v0.3.0.md"
            echo "所有发布链接和文案都已准备"
            ;;
        2)
            echo -e "\n${GREEN}API自动发布${NC}"
            check_auto_tools
            publish_hackernews
            publish_reddit
            publish_twitter
            ;;
        3)
            use_third_party_service
            ;;
        4)
            setup_github_actions
            ;;
        5)
            echo -e "\n${BLUE}所有发布选项${NC}"
            echo ""
            echo "=== 手动发布 ==="
            cat RELEASE_GUIDE_v0.3.0.md
            echo ""
            echo "=== API自动发布 ==="
            check_auto_tools
            echo ""
            echo "=== 第三方服务 ==="
            use_third_party_service
            echo ""
            echo "=== GitHub Actions ==="
            setup_github_actions
            ;;
        *)
            echo "无效选择"
            exit 1
            ;;
    esac
}

# 运行
main "$@"
