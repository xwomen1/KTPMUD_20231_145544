#!/bin/bash
# File: build_deploy_short.sh
# Description: Build and deploy with API check

# ==================== CONFIGURATION ====================
INDEX_FILE="/home/student/app_deployed/index.html"
PROJECT_DIR="/home/student/KTPMUD_20231_145544"
REMOTE_USER="student"
REMOTE_SERVER="servera"
REMOTE_DEPLOY_DIR="/home/student/app_deployed"
API_URL="http://localhost:8080/parking-status"
# =======================================================

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting deployment..."

# Build application
log "Building application..."
g++ -o main *.cpp -pthread || {
    log "Build failed!"
    exit 1
}

# Prepare deployment package
DEPLOY_TEMP="/tmp/deploy_$(date +%Y%m%d%H%M%S)"
mkdir -p "$DEPLOY_TEMP"
cp "$PROJECT_DIR/index.html" "$DEPLOY_TEMP/"
cp "$PROJECT_DIR/main" "$DEPLOY_TEMP/"
cp "$PROJECT_DIR"/*.json "$DEPLOY_TEMP/"

# Create API check script
cat > "$DEPLOY_TEMP/check_api.sh" << 'EOL'
#!/bin/bash
# Check API response
API_URL="http://localhost:8080/parking-status"
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL")

if [ "$response" -eq 200 ]; then
    echo "API is working (HTTP 200)"
    exit 0
else
    echo "API check failed (HTTP $response)"
    exit 1
fi
EOL

# Deploy to remote server
TAR_FILE="$DEPLOY_TEMP.tar.gz"
tar -czf "$TAR_FILE" -C "$DEPLOY_TEMP" .
scp "$TAR_FILE" "$REMOTE_USER@$REMOTE_SERVER:/tmp/"

# Remote execution
ssh "$REMOTE_USER@$REMOTE_SERVER" << EOF
  # Stop existing and deploy new
  pkill -f "main"
  rm -rf "$REMOTE_DEPLOY_DIR"/*
 # Create deployment directory if not exists
  mkdir -p "$REMOTE_DEPLOY_DIR"
  tar -xzf "/tmp/$(basename "$TAR_FILE")" -C "$REMOTE_DEPLOY_DIR"
  chmod +x "$REMOTE_DEPLOY_DIR"/*
  
  # Update IP in index file
  sed -i 's/172\.25\.250\.9/172.25.250.10/g' "$INDEX_FILE"
  
  # Start application
  cd "$REMOTE_DEPLOY_DIR"
  nohup ./main > /dev/null 2>&1 &
  
  # Verify API
  if "$REMOTE_DEPLOY_DIR/check_api.sh"; then
    echo "Deployment successful! API is working."
  else
    echo "Deployment completed but API check failed!"
  fi
EOF

# Cleanup
rm -rf "$DEPLOY_TEMP" "$TAR_FILE"
log "Deployment process completed"
