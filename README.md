# 🎬 Movie Recommendation System

A Movie Recommendation System built using Machine Learning and Streamlit, with real-time movie posters and descriptions.

---

## 🚀 Features

- 🎯 Recommend similar movies based on user selection
- 🖼️ Fetch movie posters using TMDb API
- 🔄 Fallback poster support using OMDb API
- 🤖 AI-generated descriptions using Google Gemini
- 🎨 Clean UI using Streamlit
- ⚡ Handles missing data (no broken images)

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- TMDb API
- OMDb API
- Google Generative AI (Gemini)

---

## 📂 Project Structure
movie-recommender-system/
│
├── app.py
├── movie_dict.pkl
├── similarity.pkl (not included due to size)
├── README.md


---

## ⚙️ How It Works

1. Select a movie from the dropdown  
2. System finds similar movies using similarity matrix  
3. Fetches:
   - Poster from TMDb
   - Backup poster from OMDb
   - Description from TMDb or Gemini AI  
4. Displays recommendations in UI  

---

## 🔑 API Setup

Create API keys from:

- TMDb → https://www.themoviedb.org/
- OMDb → http://www.omdbapi.com/
- Gemini → https://aistudio.google.com/

Replace in code:

```python
TMDB_API_KEY = "your_key"
OMDB_API_KEY = "your_key"

pip install -r requirements.txt
streamlit run app.py


---

# 🎯 That’s it

👉 Just paste into `README.md`  
👉 Push to GitHub  

---

If you want:
- 🔥 More attractive README (with images + badges)
- 💼 Resume description

Just tell 👍
