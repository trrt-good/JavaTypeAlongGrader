# Java Type-Along Grader

The Java Type-Along Grader is a Python tool for comparing and grading student Java code submissions against a reference implementation. It provides a GUI and CLI for flexibility and efficiency.

---

## Installation

### Automatic Installation (Recommended)

1. Ensure **Python 3.8+** is installed.
2. Clone the repository:

   ```bash
   git clone https://github.com/trrt-good/JavaTypeAlongGrader.git
   cd JavaTypeAlongGrader
   ```

3. Run the script:

   ```bash
   ./runapp.sh
   ```

   This will install dependencies and launch the application. Supported on **Linux** and **Mac** only. It's recommended to run this script to launch the application each time.

---

### Manual Installation

1. Ensure **Python 3.8+** is installed.
2. Clone the repository:

   ```bash
   git clone https://github.com/trrt-good/JavaTypeAlongGrader.git
   cd JavaTypeAlongGrader
   ```

3. Make virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the GUI:

   ```bash
   python typealong_app.py
   ```

6. Use the CLI (optional):

   ```bash
   python typealong_grader.py <source_code> <student_directory> <total_points>
   ```

---

## Features

- Compare Java submissions against reference code.
- Detects formatting issues, spacing errors, and Allman-style brace violations.
- Export results in CSV, Excel, JSON, and more.
- Configurable grading and detailed feedback.

---

Happy Grading! 🚀
