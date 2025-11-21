#!/usr/bin/env python3
"""
SmartPick Suite - Complete End-to-End Application
Features:
- User Authentication (Login/Register/Logout)
- Movie Tracking (Watch History)
- Grocery Basket Management
- Database Storage (SQLite)
- Responsive Design with Tailwind CSS
"""

from app import app

if __name__ == '__main__':
    print("🎯 Starting SmartPick Suite...")
    print("📱 Features: User Auth, Movie Tracking, Grocery Basket")
    print("🌐 Open: http://localhost:5000")
    print("👤 Create account or login to track your activity!")
    app.run(debug=True, host='0.0.0.0', port=5000)