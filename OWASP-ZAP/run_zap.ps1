New-Item -ItemType Directory -Force reports | Out-Null

docker run --rm `
  --add-host=host.docker.internal:host-gateway `
  -v "${PWD}/reports:/zap/wrk:rw" `
  ghcr.io/zaproxy/zaproxy:stable `
  zap-baseline.py `
  -t http://host.docker.internal:8001 `
  -J zap_report.json `
  -I