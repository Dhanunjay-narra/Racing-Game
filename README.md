# Velocity Nexus — Production 3D Racing Game & Esports Platform

Velocity Nexus is a high-performance racing simulation platform built with an authoritative client-server architecture. It combines advanced vehicle kinematics (Pacejka Magic Formula tire friction, multi-link suspension kinematics, aerodynamic downforce & drag), an innovative **Driver DNA** adaptive racing ecosystem, real-time authoritative multiplayer servers (60Hz UDP/WebSocket), procedural track generation, virtual economy with server-authoritative ledger, kinematics anti-cheat verification, and an interactive 3D WebGL client.

---

## 1. System Architecture Overview

```
                         +----------------------+
                         |     Game Clients     |
                         |                      |
                         | WebGL / PC / Mobile  |
                         +----------+-----------+
                                    |
                         +----------v-----------+
                         |   API Gateway / CDN  |
                         +----------+-----------+
                                    |
       +----------------------------+----------------------------+
       |                            |                            |
+------v-------+            +-------v--------+           +-------v--------+
| Authentication|            | Game Services  |           | Social Services|
|   Service     |            |                |           |                |
+------^--------+            +-------^--------+           +-------^--------+
       |                             |                            |
       |                    +--------v--------+                   |
       |                    | Matchmaking     |                   |
       |                    | Service         |                   |
       |                    +--------^--------+                   |
       |                             |                            |
       |                    +--------v--------+                   |
       |                    | Real-Time Game  |                   |
       |                    | Servers (60Hz)  |                   |
       |                    +--------^--------+                   |
       |                             |                            |
       +--------------+--------------+--------------+-------------+
                      |              |              |
                +-----v-----+ +------v-----+ +-----v---------+
                | PostgreSQL| |   Redis     | | Event Stream  |
                +-----------+ +------------+ +------+---------+
                                                    |
                                             +------v-------+
                                             | Analytics /  |
                                             | Driver DNA   |
                                             +--------------+
```

---

## 2. Key Features

- **Advanced Vehicle Physics**:
  - Euler & Runge-Kutta 4th Order (RK4) numerical integrators.
  - Pacejka '96 Magic Formula tire friction model (longitudinal and lateral slip curves).
  - Multi-gear sequential transmission with realistic torque curves, RPM inertia, and differential torque split.
  - Multi-link suspension simulation with anti-roll bars, damper compression/rebound, and weight transfer.
  - Dynamic aerodynamic drag and downforce with slipstream wake modeling.
  - 3 Driving Profiles: Arcade, Semi-Simulation, Full Simulation.

- **Driver DNA Adaptive Racing Ecosystem**:
  - Telemetry tracking across 7 dimensions: Aggression, Cornering, Overtaking, Drifting, Consistency, Wet Racing, Risk Management.
  - Real-time profile synthesis and rival AI behavior matching.

- **Authoritative Multiplayer & Real-Time Networking**:
  - 60Hz deterministic tick rate with client-side prediction, server reconciliation, and lag compensation.
  - Full race lifecycle management: Queue -> Matchmaking -> Server Allocation -> Countdown -> Racing -> Validation -> Leaderboards.

- **Economy & Progression**:
  - Multi-currency wallet (Credits, Nexus Gold, Race Tickets, Tuning Alloys, Season Tokens).
  - Server-authoritative double-entry ledger with cryptographic audit verification.
  - Centralized Reward Engine for races, daily login streaks, career milestones, and live seasonal events.

- **Anti-Cheat & Kinematic Verification**:
  - Server-side trajectory validation detecting impossible velocity, acceleration spikes, teleportation, and checkpoint bypasses.
  - Input anomaly detection and deterministic replay validation.

---

## 3. Installation & Dependencies

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL 15+ (optional for local mock / SQLite fallback included)
- Redis 7+ (optional for local in-memory fallback included)
- Docker & Docker Compose (optional)

### Setup Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### Install Frontend & Client Dependencies
```bash
npm install
```

---

## 4. Build Instructions

### Build Frontend WebGL Client
```bash
npm run build
```

### Build Docker Containers
```bash
docker-compose build
```

---

## 5. Running the Application

### Quick Start (Single Command)
To launch the full Velocity Nexus stack (FastAPI backend, real-time WebSocket game server, and interactive 3D WebGL client):
```bash
python main.py
```
Or with npm:
```bash
npm start
```

Open your browser at `http://localhost:8000` to access the full 3D interactive application with pre-configured 1-click test driver credentials.

### Running with Docker Compose
```bash
docker-compose up -d
```

---

## 6. Testing & Quality Assurance

Run the comprehensive test suite across physics, networking, anti-cheat, economy, and API layers:
```bash
pytest tests/ -v
```

Run test coverage analysis:
```bash
pytest --cov=backend --cov=game_servers --cov-report=term-missing tests/
```

Run frontend verification:
```bash
npm test
```

---

## 7. Proprietary License & Intellectual Property

Copyright (c) 2026 Velocity Nexus Corporation. All Rights Reserved.
CONFIDENTIAL AND PROPRIETARY. Unauthorized copying, distribution, modification, public display, or reverse engineering of this software, in source code or binary form, via any medium is strictly prohibited.
