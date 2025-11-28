# BeatCanvas

LLM 기반 음악 설계 + Python 오디오 엔진으로 음악 루프를 생성하는 AI 작곡보조 프로그램

## Features

- 🎵 **AI 음악 생성**: OpenAI GPT-4 Turbo를 사용한 장르/분위기 기반 음악 생성
- 🎹 **다중 악기 지원**: 드럼, 베이스, 멜로디 등 여러 악기 트랙
- ⚡ **유연한 설정**: BPM(60-180), 마디 수(4/8/16) 커스터마이징
- 🎧 **오디오 플레이어**: 브라우저 내 재생 및 MP3 다운로드
- 📜 **히스토리 기능**: 생성된 음악 히스토리 저장 (최대 20개)
- 🎨 **Modern UI**: Next.js + TailwindCSS를 활용한 세련된 인터페이스

## Tech Stack

### Backend
- **FastAPI**: Python 웹 프레임워크
- **OpenAI API**: GPT-4 Turbo를 이용한 음악 JSON 생성
- **pretty_midi**: JSON → MIDI 변환
- **fluidsynth**: MIDI → WAV 변환
- **pydub + ffmpeg**: WAV → MP3 변환

### Frontend
- **Next.js 14**: React 프레임워크 (App Router)
- **TypeScript**: 타입 안전성
- **TailwindCSS**: 스타일링

## Project Structure

```
BeatCanvas/
├── backend/              # Python FastAPI 백엔드
│   ├── app/
│   │   ├── main.py      # FastAPI 애플리케이션
│   │   ├── config.py    # 환경 설정
│   │   ├── models.py    # Pydantic 스키마
│   │   ├── api/         # API 엔드포인트
│   │   ├── services/    # 비즈니스 로직
│   │   └── utils/       # 유틸리티
│   ├── temp/            # 임시 오디오 파일
│   ├── requirements.txt
│   └── .env
├── frontend/            # Next.js 프론트엔드
│   ├── app/             # 페이지
│   ├── components/      # React 컴포넌트
│   └── lib/             # 유틸리티 & API 클라이언트
└── soundfonts/          # SoundFont 파일
    └── GeneralUserGS.sf2
```

## Prerequisites

### System Dependencies
```bash
# macOS
brew install fluidsynth ffmpeg python3

# Ubuntu/Debian
sudo apt-get install fluidsynth ffmpeg python3 python3-venv
```

### SoundFont
`GeneralUserGS.sf2` 파일을 `soundfonts/` 디렉토리에 배치해야 합니다.

다운로드: [GeneralUser GS](https://schristiancollins.com/generaluser.php)

## Installation

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## Configuration

### Backend (.env)
```env
OPENAI_API_KEY=sk-your-api-key-here
SOUNDFONT_PATH=../soundfonts/GeneralUserGS.sf2
TEMP_DIR=./temp
```

## Running the Application

### Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Backend will be available at:
- API: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`

### Start Frontend
```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Usage

1. **브라우저에서 http://localhost:3000 접속**
2. **장르 선택** (EDM, Hip-Hop, Jazz, Rock, Ambient 등)
3. **분위기 선택** (Happy, Sad, Energetic, Calm, Dark 등)
4. **옵션 설정** (선택사항):
   - BPM: 60-180 범위 또는 AI 자동 선택
   - 마디 수: 4, 8, 또는 16마디
5. **"Generate Music" 버튼 클릭**
6. **10-20초 대기 후 음악 재생**

## API Endpoints

### POST /api/generate
음악 생성

**Request:**
```json
{
  "genre": "EDM",
  "mood": "Energetic",
  "tempo": 128,  // optional
  "bars": 8
}
```

**Response:** MP3 binary file

**Headers:**
- `X-Tempo`: 생성된 음악의 BPM
- `X-Bars`: 마디 수
- `X-Key`: 조성
- `X-Scale`: 스케일 (major/minor)

### GET /api/health
Health check

## Development

### Backend Testing
```bash
cd backend
source venv/bin/activate

# Test MIDI generation
python -m app.services.midi_service

# Test OpenAI integration (requires API key)
python -m app.services.openai_service
```

### Frontend Development
```bash
cd frontend
npm run dev    # Development server
npm run build  # Production build
npm run start  # Production server
```

## Troubleshooting

### Backend 오류

**SoundFont not found**
- `soundfonts/GeneralUserGS.sf2` 파일이 있는지 확인
- `.env`의 `SOUNDFONT_PATH` 경로가 올바른지 확인

**OpenAI API Error**
- `.env`의 `OPENAI_API_KEY`가 올바른지 확인
- API 키에 충분한 크레딧이 있는지 확인

**fluidsynth/ffmpeg not found**
- 시스템 의존성이 설치되었는지 확인
- `which fluidsynth`, `which ffmpeg`로 확인

### Frontend 오류

**CORS Error**
- 백엔드가 실행 중인지 확인 (http://localhost:8000)
- 백엔드의 CORS 설정 확인

**localStorage Error**
- 브라우저 개발자 도구에서 localStorage 확인
- 프라이빗 브라우징 모드에서는 작동하지 않을 수 있음

## Limitations

- 4/4 박자만 지원
- 생성 후 음악 편집 불가
- 로컬 스토리지만 사용 (클라우드 백업 없음)
- 단일 사용자 (인증 없음)
- 동기 생성 (7-20초 대기 시간)
- 히스토리 최대 20개

## Future Enhancements

- [ ] 다양한 박자 지원
- [ ] 비주얼 에디터 (피아노롤)
- [ ] MIDI 파일 내보내기
- [ ] 악기별 볼륨 조절
- [ ] 사용자 계정 및 클라우드 저장
- [ ] 실시간 생성 진행률 표시

## License

MIT License

## Credits

- OpenAI GPT-4 Turbo
- pretty_midi library
- FluidSynth
- GeneralUser GS SoundFont by S. Christian Collins
