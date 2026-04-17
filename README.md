# Hemohub

**Hemohub** is a privacy-focused, decentralized blood donation and emergency response platform. Designed to bridge the gap between donors, patients, and hospitals in real-time, it prioritizes user privacy, traceability, and network reliability through modern web technologies.

---

## 🌟 Key Features

### 🛡️ Privacy-First Matching
- **Anonymous IDs**: Every donor is assigned a unique Donor ID. No personal identifiers (names, emails) are displayed publicly.
- **Mutual Confirmation**: Sensitive information like phone numbers are masked by default. They are only revealed when both donor and recipient mutually confirm the match.

### 📍 Intelligent Emergency Response
- **Geospatial Matching**: Real-time proximity search using the Haversine formula to identify the nearest compatible donors.
- **Radius Expansion**: Automatically expands search radius and triggers emergency broadcasts if no immediate match is found.
- **Top-Donor Prioritization**: Donors with high reliability scores are given priority routing if they ever require blood themselves.

### 🩸 End-to-End Traceability
- **Lifecycle Tracking**: Every blood unit is assigned a unique UUID, allowing hospitals and patients to track its journey from collection to delivery.
- **Immutable Log**: Maintains a transparent history for medical safety and accountability.

### 💎 Premium Experience
- **Glassmorphic UI**: High-fidelity dark-themed interface with modern micro-animations and a responsive design.
- **Donor Dashboard**: Monitor your reliability score, donation history, and toggle your live availability.

---

## 🛠️ Tech Stack

- **Backend**: Python (FastAPI), SQLAlchemy, SQLite
- **Frontend**: HTML5, CSS3 (Vanilla + Glassmorphism), JavaScript (ES6+)
- **Matching**: Geospatial Proximity Engine
- **Future Ready**: Designed for Web3/SSI (Self-Sovereign Identity) integration.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Modern Web Browser

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/promarc05-cell/Hemohub.git
   cd Hemohub
   ```

2. **Setup Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the Project

You will need two terminal windows:

#### Window 1: Start the API
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

#### Window 2: Start the Web App
```bash
cd frontend
python -m http.server 8080
```

Access the platform at **`http://localhost:8080`**.

---

## 📁 Project Structure

```text
Blood donation/
├── backend/            # FastAPI Application logic
│   ├── main.py         # API Endpoints & Matching logic
│   ├── models.py       # Database Schemas
│   ├── matching.py     # Proximity Engine
│   └── database.py     # SQL Connection setup
├── frontend/           # Modern UI components
│   ├── index.html      # Landing Page & Structure
│   ├── main.js         # Navigation & Flow logic
│   └── style.css       # Premium Design Tokens
└── README.md           # Project Documentation
```

---

## 🔮 Future Roadmap

- **Web3 Auth**: Integration with cryptographic wallets for decentralized identity.
- **Blockchain Ledger**: Moving traceability logs to an immutable blockchain for 100% transparency.
- **FCM Notifications**: Real-time emergency alerts via Firebase.

---

## 📜 License
*Proprietary / Open Source - Check repository settings.*
