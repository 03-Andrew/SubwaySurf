# Body Pose Controller - Subway Surfer

Control the Subway Surfer game using your body movements!  
This app uses your webcam and chest + wrist positions to simulate movement controls.

---

## 📂 Project Structure

```
project/
├── src/
│   └── main_mac.py   # Main Python application
├── README.md
└── requirements.txt  # Optional: Dependencies list
```

---

## 🚀 How to Run

### 1. Install Dependencies

Make sure you have Python 3.x installed.  
In your terminal:

```bash
pip install -r requirements.txt 
```

### 2. Run the App

Navigate to the project folder and run:

```bash
cd src
python main_mac.py
```

---

## 🎮 How to Play

1. **Open the Subway Surfer Game**

   - Go to the Subway Surfer online game:  
     👉 [https://poki.com/en/g/subway-surfers](https://www.friv.cm/subway-surfers-online/)

2. **Prepare**

   - Make sure the browser window with the game is selected (click on the game screen once).
   - Then run the Python app:  
     `python src/main_mac.py`

3. **Controls**

   - **Move Left/Right:** Move your **chest (torso)** left or right. In the camera view, you can see grid lines. Moving from one grid section to another will make you move left or right.
   - **Jump:** Raise both your wrists above your chest level.
   - **Duck:** Lower your shoulders.

   Visual Indicators:
   - A small **cross** will appear on your chest position.
   - Dots will appear on your wrists to guide you visually.

4. **Exit**

   - Press `ESC` key anytime to close the app.

---

## 📝 Notes

- Ensure you have **good lighting** for accurate pose detection.
- Works best when you sit or stand in front of your webcam with minimal background clutter.
- For Mac users, sometimes you may need to give **camera permissions** to Terminal.

---

Enjoy playing Subway Surfer using your body!

