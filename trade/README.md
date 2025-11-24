# 빗썸 자동매매 시스템

RSI 기반 자동매매 봇

## 설치

```bash
# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

## 설정

```bash
# .env 파일 생성
cp .env.example .env

# API 키 입력
BITHUMB_API_KEY=your_api_key
BITHUMB_SECRET_KEY=your_secret_key
```

## 실행

```bash
python main.py
```

서버: http://localhost:8000

## API

| 엔드포인트 | 메서드 | 설명 |
|------------|--------|------|
| `/` | GET | 상태 조회 |
| `/start` | POST | 자동매매 시작 |
| `/stop` | POST | 자동매매 중지 |
| `/buy` | POST | 수동 매수 |
| `/sell` | POST | 수동 매도 |

### 수동 매매 예시

```bash
# 전액 매수
curl -X POST http://localhost:8000/buy

# 50% 매수
curl -X POST http://localhost:8000/buy -H "Content-Type: application/json" -d '{"percent": 50}'

# 10000원어치 매도
curl -X POST http://localhost:8000/sell -H "Content-Type: application/json" -d '{"amount": 10000}'
```

## 매매 로직

- RSI < 30: 매수
- RSI > 70: 매도
