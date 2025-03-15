# Advanced Python Calculator

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Usage Instructions](#usage-instructions)
4. [Design Patterns](#design-patterns)
5. [Logging & Environment Variables](#logging--environment-variables)
6. [Exception Handling (LBYL vs EAFP)](#exception-handling-lbyl-vs-eafp)
7. [Calculation History with Pandas](#calculation-history-with-pandas)
8. [Plugin System](#plugin-system)
9. [Tests & Code Coverage](#tests--code-coverage)
10. [Demo Video](#demo-video)


---

## Project Overview

This **Advanced Python Calculator** is a command-line application (REPL) showcasing professional software development techniques, including:

- **Clean Code & Linting**: Follows PEP 8 guidelines, enforced via pylint.
- **Object-Oriented Design & Patterns**: Implements multiple design patterns (Command, Factory, Facade, Singleton, Plugin).
- **Comprehensive Logging**: Configurable log level and output destination through environment variables.
- **Persistent History Management**: Uses Pandas to manage and store calculation history in a CSV file.
- **Extensible Architecture**: Supports dynamically loaded plugins (e.g., trigonometry) without modifying core code.
- **High Test Coverage**: Unit tests, integration tests, and coverage checks via pytest and pytest-cov.

---

## Setup Instructions

1. **Clone the Repository**  
   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
   ```

2. **Create and Activate a Virtual Environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # (Linux/Mac)
   # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   Make sure your **requirements.txt** includes packages like `pandas`, `pytest`, `pytest-cov`, `pylint`.

4. **(Optional) Configure Logging**  
   ```bash
   export LOG_LEVEL=DEBUG
   export LOG_FILE=logs/calculator.log
   ```
   Without `LOG_FILE`, logs print to console; with it, logs also go to `logs/calculator.log`.

---

## Usage Instructions

1. **Run the Calculator**  
   ```bash
   python -m calculator.main
   ```
   You’ll see a welcome message. Type `menu` for commands, or `usage` for instructions.

2. **Basic Arithmetic**  
   - `add 2 3` → prints “Result: 5”  
   - `mul 4 5` → prints “Result: 20”  

3. **Advanced Operations**  
   - `sqrt 16` → prints “Result: 4”  
   - `log 100` → prints “Result: 2”

4. **History Commands**  
   - `history` → Displays in-memory history as a small Pandas DataFrame.  
   - `save_history` → Saves to CSV (`history/history.csv`).  
   - `load_history` → Loads from CSV.  
   - `clear_history` → Empties in-memory record only.  
   - `delete_history_file` → Removes the CSV file on disk.

5. **Plugin Commands**  
   - `sample_plugin` → Example plugin logs a message.  
   - `trig` → Prompts for an operation like `sin 30`.  

6. **Exit**  
   - `exit` → Quits the REPL.

---

## Design Patterns

1. **Command Pattern**  
   - **Where**: Each operation (add, sub, mul, etc.) is a separate class in [commands.py](calculator/commands.py).  
   - **Why**: Decouples operation logic from the REPL, making it easy to add new commands.

2. **Factory Pattern**  
   - **Where**: [CommandFactory in main_logic.py](calculator/main_logic.py) matches a command string (e.g. “add”) to a command object.  
   - **Why**: Centralizes object creation and ensures consistent usage.

3. **Facade Pattern**  
   - **Where**: [HistoryFacade](calculator/history_facade.py) wraps Pandas operations for loading/saving history.  
   - **Why**: Simplifies REPL code by exposing straightforward `load_history()`, `save_history()`, etc.

4. **Singleton Pattern**  
   - **Where**: [LoggerSingleton in logger.py](calculator/logger.py) ensures one logger instance.  
   - **Why**: Avoids multiple competing log handlers.

5. **Plugin Pattern**  
   - **Where**: [plugins folder](calculator/plugins/) contains `.py` files (e.g. `trig_plugin.py`). The REPL auto-loads classes named `PluginCommand`.  
   - **Why**: Adds new features (like trigonometry) without modifying core code.

---

## Logging & Environment Variables

- **Environment Variables**:  
  - `LOG_LEVEL` → “DEBUG”, “INFO”, “WARNING”, “ERROR”, “CRITICAL”  
  - `LOG_FILE` → If set, logs are written to that file; otherwise, logs go to console.

- **Where**: [LoggerSingleton](calculator/logger.py).  
- **Why**: Allows easy debugging and monitoring by adjusting log detail or location at runtime without code changes.

---

## Exception Handling (LBYL vs EAFP)

1. **LBYL (“Look Before You Leap”)**  
   - In [HistoryFacade.load_history()](calculator/history_facade.py), we check if the CSV file exists before loading it, preventing spurious errors.

2. **EAFP (“Easier to Ask for Forgiveness...”)**  
   - In [repl.py](calculator/repl.py), we attempt to parse user input as floats and catch `ValueError`. We don’t pre-check; we just try and handle the exception if it fails.

This approach balances safety checks (LBYL) for file operations and direct attempts (EAFP) for user input.

---

## Calculation History with Pandas

- **DataFrame**: Stores each operation (“operation”, “operand1”, “operand2”, “result”).  
- **CSV Management**:  
  - `save_history()` → writes to disk, default `history/history.csv`.  
  - `load_history()` → reads back into the DataFrame.  
- **Where**: [HistoryFacade](calculator/history_facade.py).  
- **Why**: Pandas allows easy data manipulation, display, and optional expansions (sorting, filtering, etc.).

---

## Plugin System

1. **Auto-Discovery**: [repl.py](calculator/repl.py) scans `calculator/plugins/` for `.py` files.  
2. **Implementation**: Each plugin has a class named `PluginCommand` with a `command_name` attribute.  
3. **Example**: 
   - [sample_plugin.py](calculator/plugins/sample_plugin.py) logs a message.  
   - [trig_plugin.py](calculator/plugins/trig_plugin.py) offers trigonometric functions (e.g., sin, cos, tan, etc.).

---

## Tests & Code Coverage

- **Running Tests**:  
  ```bash
  pytest
  ```

- **Coverage**:  
  ```bash
  pytest --cov=calculator --cov-report=term-missing
  ```
  Aiming for ≥90% coverage. 

- **Linting**:  
  ```bash
  pytest --pylint
  ```
  Ensures PEP8 compliance and consistent code style.

Test files are located under [`tests/`](tests/) with coverage for:
- **Arithmetic Commands** (add, sub, etc.)
- **REPL** 
- **Plugin Loading** 
- **History Management** 
- **Main Entrypoint** (`main.py`)

---

## Demo Video

A short (3–5 minute) video demonstrating this calculator’s features is available at:
- **[Google Drive Video Link]((https://drive.google.com/file/d/1bObYTNztKHvcxd4jIpV9f1McpXWRdIee/view?usp=sharing))**

In the video, you’ll see how to:
- Run the application and display the menu.
- Perform basic and advanced arithmetic.
- Save/load history and manage CSV files.
- Use plugins (like the trigonometry plugin).
- Observe logging behavior (if configured).

---

For questions, contributions, or issues, please open a Pull Request or raise an Issue in the repository. 

Thank you for using the **Advanced Python Calculator** and exploring its design, logging, testing, and extensibility features!
