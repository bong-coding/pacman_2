# 인공지능#2 - Multi-Agent Pacman

**Minimax**, **Expectimax** 등의 탐색 알고리즘을 활용해 유령이 포함된 Pacman 환경에서 Agent를 구현합니다.

---

##  📁 디렉토리 구조

```
multiagent/
├── multiAgents.py           # 모든 Multi-agent 탐색 Agent 구현
├── pacman.py                # 게임 실행 및 GameState 정의
├── game.py                  # 게임 로직, 방향, 그리드 정의
├── util.py                  # 스택, 큐 등 유틸리티 구조
├── autograder.py            # 자동 채점기
├── test_cases/              # 테스트 케이스 디렉토리
├── testClasses.py           # 채점 클래스
├── testParser.py            # 테스트 파서
├── graphicsDisplay.py       # 그래픽 디스플레이 
├── graphicsUtils.py         # 그래픽 유틸리티 
├── textDisplay.py           # 텍스트 디스플레이 
├── ghostAgents.py           # 유령 행동 정의 
├── keyboardAgents.py        # 키보드 제어 Agent 
├── layout.py                # 맵 레이아웃 파서 
└── 기타 지원 파일들

```
---

## 구현 파일 및 문제

구현 파일 요약

1. **Q1 - ReflexAgent**
   - 파일: `multiAgents.py`
   - 내용: 음식/유령 위치 기반 평가함수를 적용한 반응형 Agent
   - 실행: `python3 autograder.py -q q1`

2. **Q2 - MinimaxAgent**
   - 파일: `multiAgents.py`
   - 내용: 다중 유령을 고려한 Minimax 알고리즘 구현
   - 실행: `python3 autograder.py -q q2`

3. **Q3 - AlphaBetaAgent**
   - 파일: `multiAgents.py`
   - 내용: Alpha-Beta 가지치기 적용 Minimax
   - 실행: `python3 autograder.py -q q3`

4. **Q4 - ExpectimaxAgent**
   - 파일: `multiAgents.py`
   - 내용: 무작위 움직임 유령에 대응하는 Expectimax 구현
   - 실행: `python3 autograder.py -q q4`

5. **Q5 - betterEvaluationFunction**
   - 파일: `multiAgents.py`
   - 내용: 깊이 기반 탐색을 위한 고도화된 상태 평가 함수 구현
   - 실행: `python3 autograder.py -q q5`

---

## 실행 명령어

```bash
# 기본 게임 실행
python3 pacman.py

# Q1: ReflexAgent
python3 pacman.py -p ReflexAgent -l testClassic

# Q2: MinimaxAgent
python3 pacman.py -p MinimaxAgent -l minimaxClassic -a depth=3

# Q3: AlphaBetaAgent
python3 pacman.py -p AlphaBetaAgent -l smallClassic -a depth=3

# Q4: ExpectimaxAgent
python3 pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3

# Q5: 평가함수 성능 평가
python3 autograder.py -q q5 --no-graphics

```