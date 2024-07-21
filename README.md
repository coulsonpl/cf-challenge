### Docker部署

```yaml
# version: '3'
services:
  cf-challenge:
    container_name: cf-challenge
    image: coulsontl/cf-challenge
    network_mode: host
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
      # 注意：浏览器的代理设置不支持用户名密码认证
      - HTTPS_PROXY=http://192.168.31.3:7890
      - SERVER_PORT=3009
```

### 接口调用

```bash
# 获取PopAi的GToken
curl  http://192.168.31.3:3009/challenge/pop/gtoken

# 获取zhile.io的cf_clearance
curl http://192.168.31.3:3009/challenge/cf/clearance
```