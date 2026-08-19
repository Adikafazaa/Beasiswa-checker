# 🎓 Beasiswa Checker Analytics (Terminal Edition)
## 📘 Complete Technical Documentation & Implementation Architecture

---

## ⚙️ 1. BACKEND ARCHITECTURE & ENGINE LOGIC

### 🗄️ Database & Storage Layer (`modules/storage/migrator.py` & `modules/database.py`)
- **Engine**: SQLite 3 operating in High-Performance **WAL (Write-Ahead Logging)** mode with busy timeout handling (5000ms).
- **Migration Engine**: Zero-dependency migration system maintaining 6 core tables:
  1. `user_profiles`: Stores applicant credentials, academic scores (GPA, IELTS, TOEFL iBT), target countries, and persistent `last_ai_analysis` cache.
  2. `scholarships`: Master database of international and national scholarships.
  3. `user_scholarship_flags`: Per-user isolated bookmark flags, application statuses (`SAVED`, `APPLIED`, `ACCEPTED`, `REJECTED`), priorities (`HIGH`, `MED`, `LOW`), and personal notes.
  4. `user_match_history`: Analytical historical log of computed match percentages.
  5. `scrape_logs`: Ingestion audit log table for web scraping pipelines.
  6. `schema_migrations`: Version migration control ledger.

---

### 🧮 Core Scholarship Matching Engine (`modules/matching_engine.py`)
- **Algorithm**: Weighted multi-factor analytical scoring engine returning compatibility fit (0% – 100%).
- **Factors Evaluated**:
  - GPA / IPK threshold compatibility.
  - IELTS & TOEFL iBT language score compliance.
  - Academic level alignment (S1 / S2 / S3).
  - Work experience & research publication count.
- **Categorization Rules**:
  - **`Safety` Fit**: Score $\ge 85\%$ (High acceptance probability).
  - **`Target` Fit**: $70\% \le \text{Score} < 85\%$ (Good fit).
  - **`Reach` Fit**: Score $< 70\%$ (Ambitious target).

---

### 🛡️ 100% Token-Protected AI Advisor Subsystem (`modules/ai_client.py` & `modules/ai_advisor.py`)
- **API Provider**: DeepSeek API (`DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`).
- **Model Target**: `deepseek-v4-flash`.
- **Latency Protection**: Configured `httpx.Client(timeout=15.0)` to accommodate DeepSeek multi-paragraph reasoning outputs safely.
- **0-Token Protection System**: Main dashboard startup and routine navigation spend **0 API tokens** by using `generate_rule_based_advice()` (offline rule-based engine). DeepSeek API is called **only on-demand** when explicitly triggered under menu `[5]`.
- **Persistent AI Storage**: Saves generated DeepSeek AI analysis into `user_profiles.last_ai_analysis` in SQLite.

---

### 🌐 Web Scraper Subsystem (`modules/scraper/`)
- **Engine**: Playwright Headless Browser & HTML Parser Pipeline.
- **Politeness Guard**: Checks `robots.txt` compliance before requesting external domain URLs.

---

### 🧪 System Unit Test Suite (`tests/test_full_suite.py`)
- **Coverage**: 5-layer offline verification suite testing Pydantic V2 models, SQLite migration, Matching Engine, Multi-user bookmark isolation, and Scraper politeness guard in under 0.2s without spending any API tokens.

---

## 🖥️ 2. FRONTEND / TUI INTERFACE & USER EXPERIENCE

### 📐 Responsive Wireframe Dashboard (`cli/views.py`)
- **Layout Grid**: Rich `Layout` engine splitting terminal into Header Banner, Left Matrix Table, Right Sidebar (`Informasi Pendaftar` & `Analisis & Rekomendasi AI`), and Bottom Navigation Bar.
- **⚡ Zero-Flicker Redrawing (`soft_clear_screen`)**: Uses VT100 ANSI cursor positioning (`\033[H`) to update terminal screens in-place in ~1ms without black flickering.

---

### 📄 Paginated Database Table & Interactive Entry Cards
- **Pagination**: Table displays **8 items per page** with `[P]` (Previous Page) and `[N]` (Next Page) controls.
- **Row-Indexed Selection**: Users can type row index numbers `[1]` to `[8]` directly on the table to inspect full detail cards.

---

### 🎨 100% Emoji-Free Clean TUI Styling & Vibrant Color Scheme
- **ASCII/Unicode Text Badges**: Replaced mobile consumer emojis with clean terminal text badges:
  - `[TARGET UTAMA]`, `[IELTS]`, `[PUBLIKASI]`, `[PENGALAMAN]`, `[CATATAN SYARAT]`
  - `[BOOKMARKED]`, `[NO BOOKMARK]`
  - `[✓]` Success, `[!]` Warning, `[x]` Error.
- **Color Palette**:
  - **Bright Bold Yellow**: `[TARGET UTAMA]`, panel title headers, navigation selection pointer `▶`.
  - **Bright Bold Cyan**: `[IELTS]`, `[PUBLIKASI]`, `[PENGALAMAN]`, section headers.
  - **Bright Bold Green**: `[88.0% Match]`, `[SAVED]`, success badges.
  - **Bright Bold Red**: `[CATATAN SYARAT]`, deadlines, error warnings.

---

### ⌨️ Navigation & Keyboard Shortcuts (`cli/menus.py` & `main.py`)
- **Interactive Navigation**: Left / Right / Up / Down Arrow key navigation with Enter selection.
- **5 Consolidated Main Menus**: `[1] Dashboard`, `[2] Profil`, `[3] Filter`, `[4] Bookmark`, `[5] Fitur AI & Scraper`, `[0] Keluar`.
- **Explicit `[0] Kembali ke Dashboard Utama`**: Provided inside Filter search choices for instant return.
- **Keybind `[E]` (Expanded Dual AI Analysis Screen)**: Pressing **`E`** (or **`e`**) opens full-screen view displaying **both** the 0-token rule engine action plan and full DeepSeek AI report.

---

## ⭐ 3. USER-REQUESTED CUSTOM FEATURES IMPLEMENTED

1. **First-Time Launch Profile Setup**: Prompts users to enter initial profile data when launched for the first time.
2. **Grouped AI & Automation Hub (`[5] Fitur AI & Scraper`)**: Consolidates all features using AI or external network calls under option `[5]` for token safety.
3. **Dashboard Persistent AI Analysis**: Automatically displays the latest generated DeepSeek AI analysis on the Dashboard sidebar.
4. **Keybind `[E]` Dual-Perspective View**: Resolves sidebar box overflow by capping preview lines and offering full-screen view via shortcut key **`E`**.
