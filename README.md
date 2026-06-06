# 🚌 Campus Ride — Distributed Systems Project

> A cloud-native ride-sharing platform for UUM students, built with FastAPI, Next.js, PostgreSQL, Docker, and Kubernetes, deployed on Railway.

**Live URL:** https://frontend-production-1637.up.railway.app  
**Backend API:** https://backend-production-7e5f.up.railway.app  
**Course:** STIJK2124 — Distributed Computing  
**University:** Universiti Utara Malaysia (UUM)

---

## 📐 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│                   Browser / Mobile App                          │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTPS (TLS)
┌─────────────────────────▼───────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│              Next.js Frontend (Port 3000)                       │
│         Auth: Supabase JWT    Styling: Tailwind CSS             │
│         Railway URL: frontend-production-1637.up.railway.app    │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP REST API
┌─────────────────────────▼───────────────────────────────────────┐
│                      BUSINESS LAYER                             │
│              FastAPI Backend (Port 8000)                        │
│         Auth Middleware   Route Logic   Supabase Client         │
│         Railway URL: backend-production-7e5f.up.railway.app     │
└─────────────────────────┬───────────────────────────────────────┘
                          │ SQL (Port 5432)
┌─────────────────────────▼───────────────────────────────────────┐
│                       DATA LAYER                                │
│              PostgreSQL Database (Port 5432)                    │
│         Supabase Auth    Row Level Security    Migrations       │
└─────────────────────────────────────────────────────────────────┘

INFRASTRUCTURE LAYERS:
┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐
│   Docker     │  │  Kubernetes  │  │        Railway           │
│  Compose     │  │   (kind)     │  │   (Production Deploy)    │
│ campus-      │  │  Deployment  │  │  Auto-scaling, CI/CD     │
│ backend      │  │  Service     │  │  Metrics Dashboard       │
│ campus-      │  │  HPA (2-10   │  │                          │
│ frontend     │  │   replicas)  │  │                          │
│ campus-      │  │  ConfigMap   │  │                          │
│ postgres     │  │  Secret      │  │                          │
└──────────────┘  └──────────────┘  └──────────────────────────┘
```

---

## 🛠️ Prerequisites

| Tool | Version | Installation |
|------|---------|-------------|
| Python | 3.11+ | https://python.org |
| Node.js | 20+ | https://nodejs.org |
| Docker Desktop | 4.x+ | https://docker.com/products/docker-desktop |
| kubectl | 1.28+ | https://kubernetes.io/docs/tasks/tools |
| kind | 0.20+ | https://kind.sigs.k8s.io/docs/user/quick-start |
| Artillery | Latest | `npm install -g artillery` |
| Wireshark | 4.x+ | https://wireshark.org |
| Git | 2.x+ | https://git-scm.com |

---

## ⚙️ Environment Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Your Supabase project URL | Supabase Dashboard → Settings → API |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous/public key | Supabase Dashboard → Settings → API |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | Supabase publishable key | Supabase Dashboard → Settings → API |
| `SUPABASE_URL` | Supabase URL (backend) | Supabase Dashboard → Settings → API |
| `SUPABASE_KEY` | Supabase service role key | Supabase Dashboard → Settings → API |
| `DATABASE_URL` | PostgreSQL connection string | Format: `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | JWT secret key for FastAPI | Generate: `openssl rand -hex 32` |

Create a `.env.local` file in the `frontend/` folder and a `.env` file in the `backend/` folder using `.env.local.example` as a template.

---

## 🚀 Setup Instructions (Parts 1–7)

### Part 1 — Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/afrinaatiqah/campus-ride.git
cd campus-ride

# 2. Set up backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Supabase credentials

# 3. Run backend
uvicorn app.main:app --reload --port 8000

# 4. Set up frontend (new terminal)
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your Supabase credentials

# 5. Run frontend
npm run dev
```

Visit: http://localhost:3000

---

### Part 2 — Supabase Authentication

```bash
# 1. Create a Supabase project at https://supabase.com
# 2. Copy your Project URL and anon key
# 3. Add to frontend/.env.local:
NEXT_PUBLIC_SUPABASE_URL=your_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key

# 4. Run database migrations in Supabase SQL editor
# (see /supabase/migrations/ folder)

# 5. Test auth at http://localhost:3000/login
```

---

### Part 3 — Docker Containerization

```bash
# 1. Make sure Docker Desktop is running

# 2. Build and start all containers
docker-compose up -d

# 3. Verify containers are running
docker ps

# 4. Test backend
curl http://127.0.0.1:8000/health
# Expected: {"status":"ok","database":"connected"}

# 5. Check container IPs
docker network inspect dist_sys_app_default

# 6. Stop containers
docker-compose down
```

---

### Part 4 — Kubernetes Orchestration

```bash
# 1. Create kind cluster
kind create cluster --name campus-ride

# 2. Load images into kind
kind load docker-image afrinaatiqah/campus-backend:latest --name campus-ride
kind load docker-image afrinaatiqah/campus-frontend:latest --name campus-ride

# 3. Apply Kubernetes manifests
kubectl apply -f k8s/

# 4. Verify pods are running
kubectl get pods
kubectl get services

# 5. Port forward to access locally
kubectl port-forward service/campus-backend 8000:8000
```

---

### Part 5 — Railway Cloud Deployment

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy backend
cd backend
railway up --service backend

# 4. Deploy frontend
cd frontend
railway up --service frontend

# 5. Set environment variables in Railway Dashboard
# (Project → Service → Variables)
```

Live URLs:
- Frontend: https://frontend-production-1637.up.railway.app
- Backend: https://backend-production-7e5f.up.railway.app

---

### Part 6 — Wireshark Network Analysis

```bash
# 1. Install Wireshark from https://wireshark.org

# 2. Start local containers
docker-compose up -d

# 3. Open Wireshark → select "Adapter for loopback traffic capture"
# 4. Leave capture filter empty, start capture

# 5. Test endpoints (PowerShell)
curl http://127.0.0.1:8000/health

# POST with JSON
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/students/" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"name":"Ali","matric_id":"S001","email":"ali@uni.edu","lat":6.45,"lng":100.50}'

# 6. Stop capture and apply display filters (see Wireshark Filter Reference below)
```

---

### Part 7 — Load Testing

```bash
# 1. Install Artillery
npm install -g artillery

# 2. Create load-test.yml (see file in root directory)

# 3. Run load test
artillery run load-test.yml

# 4. Monitor Railway Dashboard → backend → Metrics during test
```

---

## 📁 Kubernetes Manifest Files

| File | Description |
|------|-------------|
| `k8s/backend-deployment.yaml` | Deploys FastAPI backend with 2 replicas |
| `k8s/backend-service.yaml` | Exposes backend on port 8000 (ClusterIP) |
| `k8s/frontend-deployment.yaml` | Deploys Next.js frontend with 2 replicas |
| `k8s/frontend-service.yaml` | Exposes frontend on port 3000 (NodePort) |
| `k8s/postgres-deployment.yaml` | Deploys PostgreSQL database |
| `k8s/postgres-service.yaml` | Exposes PostgreSQL on port 5432 |
| `k8s/configmap.yaml` | Non-sensitive environment configuration |
| `k8s/secret.yaml` | Sensitive credentials (base64 encoded) |
| `k8s/hpa.yaml` | HorizontalPodAutoscaler — scales backend 2–10 replicas at 70% CPU |

---

## 🔍 Wireshark Filter Reference

| Exercise | Filter | What It Captures |
|----------|--------|-----------------|
| 6.1 — TCP Handshake | `tcp.flags.syn == 1 and tcp.port == 8000` | SYN, SYN-ACK, ACK packets |
| 6.2 — HTTP GET | `tcp.port == 8000` | Full HTTP GET request + response layers |
| 6.3 — HTTP POST | `http.request.method == "POST"` | POST request with JSON payload |
| 6.4 — TCP Close | `tcp.port == 8000` | FIN-ACK → ACK connection teardown |
| 6.5 — Docker Traffic | `ip.addr == 172.18.0.2 or ip.addr == 172.18.0.3` | Container-to-container traffic |
| 6.6 — TLS/HTTPS | `tls` | Client Hello → Server Hello → Encrypted data |

---

## 🌐 Live Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Backend health check |
| `/api/v1/students/` | GET | List all students |
| `/api/v1/students/` | POST | Create a student |
| `/api/v1/rides/` | GET | List all rides |
| `/api/v1/rides/` | POST | Create a ride |
| `/auth/callback` | GET | Supabase auth callback |
| `/login` | GET | Login page |

---

## 🐛 Troubleshooting

### 1. `ImagePullBackOff` in Kubernetes
**Problem:** Kubernetes can't pull Docker images.  
**Solution:**
```bash
# Load images directly into kind cluster
kind load docker-image afrinaatiqah/campus-backend:latest --name campus-ride
kind load docker-image afrinaatiqah/campus-frontend:latest --name campus-ride
```

### 2. `docker-compose up` fails — Docker daemon not running
**Problem:** `failed to connect to docker API at npipe:////./pipe/dockerDesktopLinuxEngine`  
**Solution:** Open Docker Desktop and wait for it to fully start (whale icon steady in taskbar), then retry.

### 3. `curl` fails — `Unable to connect to remote server`
**Problem:** Backend container is not running.  
**Solution:**
```bash
docker-compose up -d
# Wait 10 seconds, then retry curl
curl http://127.0.0.1:8000/health
```

### 4. Wireshark shows no packets on loopback
**Problem:** Capture filter syntax error or wrong interface.  
**Solution:** Leave capture filter **empty**, select "Adapter for loopback traffic capture", use display filter `tcp.port == 8000` after capture.

### 5. Railway deployment shows 502 errors under load
**Problem:** Free tier Railway instances get overwhelmed at high request rates.  
**Solution:** This is expected behaviour — 502s under 50 req/s load demonstrates the need for horizontal scaling. The HPA in Kubernetes handles this automatically.

---

## 👥 Team Member Contributions

| Member | Parts | Responsibilities |
|--------|-------|-----------------|
| Putri | Parts 1, 2 | Local development setup, Supabase authentication integration |
| Afrina | Parts 3, 4, 5 | Docker containerization, Kubernetes orchestration, Railway cloud deployment |
| Azmirah | Parts 6, 7 | Wireshark network analysis, load testing & horizontal scaling |

---

## 📄 License

This project was developed for academic purposes at Universiti Utara Malaysia (UUM) for the STIJK2124 Distributed Computing course.
