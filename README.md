# Java Type-Along Grader

The Java Type-Along Grader is a Python tool for comparing and grading student Java code submissions against a reference implementation. It provides a GUI and CLI for flexibility and efficiency.

---

## Usage

1. Upload the source code file (teacher's code)

2. Link the directory containing all student files; the tool will recursively find all Java files within this directory.

3. Choose the comment ignoring level:
   - **all**: All comments are ignored. Students won't be marked off for adding their own comments or not writing teacher's comments.
   - **eol**: End-of-line comments are ignored (e.g. int counter // this is the number of iterations). Students are allowed to write whatever they want for such comments, but not for comments that exist independently (like ones above a function definition)
   - **none**: No comments are ignored. Students are expected to have identical comments of all types.

4. Run the grader and review results.

## Things to note

1. Student names are obtained from the first line of their header. The rest of their header is ignored for grading. Students who include "Conlin" in their name are marked off.
2. No points are directly deducted for the "Brackets" error because "SpacingError" and "NewLineError" mistakes already account for it.

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

### Installing GitHub on Mac (with Homebrew)

1. Install Homebrew (if not already installed):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Git using Homebrew:

   ```bash
   brew install git
   ```

3. Verify the installation:

   ```bash
   git --version
   ```

4. Configure Git with your name and email:

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

Now you're ready to use Git and GitHub on your Mac!

---

## Features

- Compare Java submissions against reference code.
- Detects formatting issues, spacing errors, and Allman-style brace violations.
- Export results in CSV, Excel, JSON, and more.
- Configurable grading and detailed feedback.

---

Happy Grading! 🚀
