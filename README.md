# GitHub Webhook Dashboard

This Flask app receives GitHub webhook events and displays recent GitHub activity using MongoDB.

## 🔧 Features
- Receives `push`, `pull_request (opened)`, and `merged` events via GitHub Webhooks.
- Stores event data in MongoDB Atlas.
- Displays latest events on a simple web dashboard.

## 📦 Tech Stack
- Python Flask
- MongoDB Atlas
- HTML + JavaScript (for frontend)

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/shyampawar756/webhook-dashboard.git
cd webhook-dashboard
