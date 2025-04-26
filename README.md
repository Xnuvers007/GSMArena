# 📱 GSM Arena Scraper API (Flask)

A simple REST API built with Flask that scrapes data from [GSMArena.com](https://www.gsmarena.com). It allows you to fetch phone **brands**, **device lists**, and **detailed specifications** including **user comments** — all directly from the web.

---

## 🌐 Live Endpoints

| Endpoint        | Method | Description                                 |
|-----------------|--------|---------------------------------------------|
| `/`             | GET    | Welcome message and available endpoints     |
| `/brands`       | GET    | List all phone brands                       |
| `/devices`      | GET    | List all devices under a specific brand     |
| `/specs`        | GET    | Get specifications and comments of a phone |

---

## 🚀 How to Run Locally

### 1. Clone Repository
```bash
git clone https://github.com/Xnuvers007/GSMArena.git
cd GSMArena
