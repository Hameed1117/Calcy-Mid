# Advanced Python Calculator

## Project Overview
This advanced Python-based calculator is developed for a Software Engineering Graduate Course. The application demonstrates professional software development practices including clean, maintainable code, the use of design patterns, comprehensive logging, dynamic configuration via environment variables, robust data handling with Pandas, and a feature-rich command-line interface (REPL) for real-time user interaction.

## Key Features
- **Calculator Operations:**  
  Basic arithmetic (add, subtract, multiply, divide) and advanced operations (square root, square, cube, logarithm) are implemented.
- **REPL Interface:**  
  A user-friendly command-line interface allows users to interact with the calculator in real time.
- **History Management:**  
  Calculation history is managed using Pandas. Users can load, save, clear, and delete their calculation history, which is stored in a dedicated `history` folder.
- **Dynamic Plugin System:**  
  The calculator supports a plugin system to extend functionality without modifying core code. A sample plugin is included as a demonstration.
- **Comprehensive Logging:**  
  Logging is integrated throughout the application with configurable log levels and output destinations (via environment variables).
- **Robust Exception Handling:**  
  The application employs both LBYL (Look Before You Leap) and EAFP (Easier to Ask for Forgiveness than Permission) styles in exception handling.
- **Design Patterns:**  
  - **Command Pattern:** Each arithmetic operation is encapsulated in its own command class.
  - **Factory Pattern:** A factory method selects and returns the correct command object based on user input.
  - **Facade Pattern:** A facade provides a simplified interface for managing complex Pandas operations.
  - **Singleton Pattern:** A singleton logger ensures a single logging instance across the application.
  - **Plugin Pattern:** Plugins are dynamically loaded to extend functionality.

## Environment Variables & Logging
The application uses environment variables to configure logging:
- `LOG_LEVEL`: Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
- `LOG_FILE`: If set, log output is written to the specified file instead of the console.
See [calculator/logger.py](calculator/logger.py) for implementation details.

## Setup & Installation
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
From the repository root, run:

```bash
python -m calculator.main
```

Alternatively, you can run:

```bash
python calculator/main.py
```

This starts the REPL interface where you can type commands (e.g., add 2 3, sqrt 16, etc.).

## Running Tests
The project includes comprehensive tests using Pytest. To run the tests:

```bash
pytest
```

## Continuous Integration
A GitHub Actions workflow is configured (located at .github/workflows/python-app.yml) to automatically run tests and linting (via pylint) on every push and pull request.

## Video Demonstration
A brief 3-5 minute video demonstration of the calculator's key features is available. The video highlights:

- The REPL interface in action.
- How to execute arithmetic operations.
- Managing calculation history.
- Dynamically loaded plugins.
- Logging and error handling mechanisms.

Watch the demonstration here: [Video Link]

## Commit History & Documentation
This repository maintains a clear commit history with logical, incremental changes that document the development process. For more details on the design patterns and logging strategy used, please refer to the inline comments in the source code.

## Conclusion
This project showcases advanced programming techniques, design patterns, and professional software development practices. Enjoy using the Advanced Python Calculator!

Happy Calculating!