# 🌍 AI Smart Trip Planner

An AI-powered travel planner that generates personalized itineraries based on user inputs like budget, duration, and travel type.

---

## 🚀 Features

- ✨ AI-generated travel plans  
- 💰 Budget-aware itinerary  
- 🎯 Travel type customization (Adventure / Relax / Family)  
- 📊 Clean table output  
- 📄 Download trip plan as PDF  

---

## 📸 Preview

![App Screenshot](Screenshot-1.png)

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Groq API (LLaMA 3)  
- Pandas  
- ReportLab  

---

## 💡 How It Works

1. User enters trip details (budget, days, type)
2. Prompt is sent to LLM via Groq API
3. AI generates structured itinerary (CSV + summary)
4. Data is parsed using pandas
5. Displayed in table format + downloadable PDF
