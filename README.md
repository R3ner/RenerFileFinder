# RenerFileFinder 🔍

A clean, modern, and lightweight desktop application built with Python to help you find files and search for specific keywords inside text-based documents.

## 🚀 Features
- **Modern UI:** Built with CustomTkinter for a sleek, dark-themed experience.
- **Fast Search:** Quickly scan directories and subdirectories for filenames.
- **Deep Search:** Search for specific strings/keywords inside files (`.txt`, `.js`, `.json`, `.py`, `.html`, etc.).
- **Easy Access:** Open the containing folder of any search result directly from the app.
- **Cross-Platform:** Works on Windows, macOS, and Linux.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/R3ner/RenerFileFinder.git](https://github.com/R3ner/RenerFileFinder.git)
   cd RenerFileFinder

2. **Install dependencies: Make sure you have Python installed, then run:**
```bash pip install -r requirements.txt```

3. **Run the application:**
    ```bash 
    python src/main.py

## 📝 Usage

1. Click Browse to select the directory where you want to search.

2. Enter the Keyword (filename or content).

3. (Optional) Check Deep search to look inside file contents.

4. Click START SEARCH.

5. Select a result from the box and click Open Selected File Location to view it in your explorer.

**📂 Project Structure**
```
RenerFileFinder/
├── src/
│   ├── main.py           # Application entry point
│   ├── search_engine.py  # Search logic & OS operations
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation ```

