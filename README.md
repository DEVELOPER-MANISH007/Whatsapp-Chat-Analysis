# WhatsApp Chat Analyzer 📊

A powerful web-based application to analyze WhatsApp chat exports and generate insightful statistics and visualizations.

## 🎯 Features

- **Message Statistics**: Total messages, words, media files, and links
- **User Analysis**: Individual user statistics and comparisons
- **Timeline Visualization**: Monthly message trends
- **Word Cloud**: Visual representation of frequently used words
- **Media Tracking**: Count of media files and links shared
- **Group Support**: Analyze individual or group conversations
- **Data Cleaning**: Automatic handling of system messages and emojis

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Web framework for building interactive UI |
| **Pandas** | Data manipulation and analysis |
| **Matplotlib** | Statistical data visualization |
| **Seaborn** | Advanced statistical graphics |
| **Plotly** | Interactive data visualizations |
| **URLExtract** | Extract URLs from messages |
| **WordCloud** | Generate word frequency clouds |
| **Emoji** | Parse and analyze emojis |

## 📁 Project Structure

```
DSPROJECT3/
└── python/
    ├── main.py                 # Main Streamlit application
    ├── preprocessor.py         # WhatsApp chat data preprocessing
    ├── helper.py               # Helper functions for analysis & visualization
    ├── requirements.txt        # Python dependencies
    ├── stopword.txt            # Common words to exclude from analysis
    └── dump/                   # Backup/reference copies
        ├── helper.py
        ├── main.py
        └── preprocessor.py
```

## 📝 File Descriptions

### `main.py`
The main Streamlit application that provides:
- UI for uploading WhatsApp chat exports
- Sidebar controls for user selection and analysis triggers
- Display of statistics and visualizations
- Integration of preprocessor and helper modules

### `preprocessor.py`
Handles data parsing and cleaning:
- Extracts messages using regex pattern matching
- Parses timestamps (format: `DD/MM/YY, HH:MM`)
- Separates user names from messages
- Creates structured DataFrame for analysis
- Handles system notifications (joins, leaves)

### `helper.py`
Core analytics functions:
- `fetch_stats()` - Calculate messages, words, media, links count
- `additional_stats()` - Average words per message, longest message
- `monthly_timeline()` - Messages trend over months
- Visualization functions for charts and word clouds

### `stopword.txt`
Common English words excluded from word cloud analysis to focus on meaningful words.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd python
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 How to Use

1. **Export WhatsApp Chat**
   - Open WhatsApp → Select Chat → Menu → More → Export Chat
   - Choose "Without Media"
   - Save as `.txt` file

2. **Run the Application**
   ```bash
   streamlit run main.py
   ```

3. **Upload & Analyze**
   - Upload the exported `.txt` file
   - Select a user from dropdown (or "Overall" for group stats)
   - Click "Show Analysis"
   - View interactive charts and statistics

## 📊 Sample Analysis Output

The application generates:
- **Metrics**: Total messages, words, media, links
- **Timeline Graph**: Message frequency over time
- **Word Cloud**: Most frequently used words
- **User Rankings**: Top contributors
- **Activity Patterns**: Busiest hours/days

## 🔧 Requirements

See `requirements.txt` for detailed version information:
- streamlit
- pandas
- matplotlib
- seaborn
- plotly
- urlextract
- wordcloud
- emoji

## 📌 Notes

- Chat export format: WhatsApp's default `.txt` format
- Supports both individual and group chats
- System messages (joins, leaves) are filtered out
- Emojis are parsed and analyzed separately

## 💡 Future Enhancements

- Support for exported images and media
- Sentiment analysis of messages
- Language detection and translation
- Database storage for multiple chats
- Advanced NLP features

## 📄 License

This project is open source and available for educational purposes.

---

**Created**: April 2026  
**Last Updated**: April 30, 2026
