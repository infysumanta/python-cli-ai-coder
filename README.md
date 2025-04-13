# Python CLI AI Coder

A powerful command-line tool that leverages artificial intelligence to generate complete project structures, add new features to existing projects, and streamline your development workflow.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Python CLI AI Coder** helps developers quickly bootstrap new projects with well-structured codebases, proper configuration files, and best practices already implemented. Save hours of setup time and focus on building your application's unique features.

## ✨ Features

- **Project Generation**: Create complete project structures for various frameworks and languages
- **Smart Templates**: Choose from multiple project types (Python, JavaScript, TypeScript, React, Express, etc.)
- **Feature Selection**: Customize your project with optional features (Git, Tests, GitHub Actions, Documentation)
- **Interactive CLI**: User-friendly command-line interface with progress tracking and visual feedback
- **Feature Addition**: Extend existing projects with new functionality
- **Project Organization**: Generate well-structured projects with proper file organization
- **Documentation**: Automatically create README files and other documentation

## 🚀 Project Types

- Python
- JavaScript
- TypeScript
- React + Vite + TypeScript
- React + Vite + JavaScript
- Express + TypeScript
- Express + JavaScript
- Custom (specify your own)

## 📋 Project Structure

```bash
python-cli-ai-coder/
├── .env                  # Environment variables (contains API key)
├── main.py               # Entry point for the application
├── requirements.txt      # Project dependencies
├── src/                  # Main source code directory
│   ├── __init__.py       # Package initialization
│   ├── cli/              # Command-line interface
│   │   ├── __init__.py
│   │   └── main.py       # CLI implementation
│   ├── core/             # Core functionality
│   │   ├── __init__.py
│   │   └── project_generator.py  # ProjectGenerator class
│   └── utils/            # Utility functions
│       ├── __init__.py
│       ├── command_operations.py  # Command execution functions
│       └── file_operations.py     # File and directory management functions
```

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/infysumanta/python-cli-ai-coder.git
   cd python-cli-ai-coder
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/Mac
   # OR
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file with your API key**:

   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## 📖 Usage

### Generate a New Project

Run the project generator:

```bash
python main.py
```

### Interactive Workflow

1. **Select a project type** from the available options:

   - Python
   - JavaScript
   - TypeScript
   - React + Vite (TypeScript or JavaScript)
   - Express (TypeScript or JavaScript)
   - Custom (specify your own)

2. **Enter a project name** that will be used for the project directory and in generated files

3. **Choose a directory** to store the project (defaults to `projects/your_project_name`)

4. **Provide a project description** that will be used to generate appropriate code and documentation

5. **Select optional features**:

   - 🔀 **Git Initialization**: Initialize a Git repository with appropriate .gitignore
   - 🚨 **Testing Framework**: Add testing framework with sample tests
   - 🛠️ **GitHub Actions**: Set up CI/CD workflows
   - 📝 **Documentation**: Create documentation structure and templates

6. **Confirm and generate** your project structure

7. **View the summary** of generated files and directories

### Feature Addition

After generating a project, you can add new features to extend its functionality:

```bash
# After project generation completes, you'll be prompted to add features
# Or run the tool again and navigate to the existing project directory
python main.py
```

### Feature Addition Workflow

1. **Select "Yes"** when asked if you want to add features to the project

2. **Describe the feature** you want to add in natural language, for example:

   - "Add a user authentication system with login and registration"
   - "Create a database connection module with SQLAlchemy"
   - "Add a REST API endpoint for user profiles"
   - "Implement a logging system with rotating file handlers"

3. **Watch as the tool analyzes** your project structure and implements the feature

4. **Review the changes** made to your project files

5. **Optionally add more features** by selecting "Yes" when prompted

## ⚙️ Configuration Options

- **Project Types**: Choose from predefined templates or create custom ones
- **Project Features**:
  - **Git**: Initialize a Git repository with appropriate .gitignore
  - **Tests**: Add testing framework with sample tests
  - **GitHub Actions**: Set up CI/CD workflows
  - **Documentation**: Create documentation structure and templates

### Technical Implementation

The Python CLI AI Coder uses a tool-based approach to generate project structures:

#### AI Tool System

The `ProjectGenerator` class defines a set of tools that the AI model can call to manipulate files and directories:

| Tool                      | Description                 | Usage                                |
| ------------------------- | --------------------------- | ------------------------------------ |
| `read_file`               | Read the contents of a file | Used to analyze existing files       |
| `get_file_metadata`       | Get metadata for a file     | Used to check file properties        |
| `list_directory_contents` | List files and directories  | Used to understand project structure |
| `write_to_file`           | Write content to a file     | Used to create or update files       |
| `create_directory`        | Create a new directory      | Used to create folder structure      |
| `run_command`             | Execute a shell command     | Used to run initialization commands  |

These tools are exposed to the AI model through a function-calling interface, allowing it to manipulate the filesystem in a controlled and secure manner.

## How It Works

![Python CLI AI Coder Workflow](https://via.placeholder.com/800x400.png?text=Python+CLI+AI+Coder+Workflow)

1. **Initialization** 🚀

   - The tool loads the OpenAI API key from the `.env` file
   - It initializes the `ProjectGenerator` class with this key
   - The system prepares the available tools for AI to use

2. **User Input Collection** 💬

   - The CLI presents an interactive interface with colorful prompts
   - Users select project type, name, location, and description
   - Users customize project features through a visual selection interface
   - All selections are validated and confirmed before proceeding

3. **Project Generation Process** ⚙️

   - The system crafts detailed prompts for the AI model with project specifications
   - The AI model (GPT-4o) analyzes the requirements and plans the project structure
   - The AI makes tool calls to create directories, files, and execute commands
   - The system executes these calls and provides real-time visual feedback
   - A comprehensive project structure is built according to best practices

4. **Feature Addition Capability** 🔍

   - Users can request new features in natural language
   - The AI analyzes the existing project structure to understand the codebase
   - The system determines the necessary changes to implement the feature
   - Files are modified or created to add the requested functionality
   - Tests and documentation are updated to reflect the new features

## 📦 Dependencies

- **rich**: Enhanced terminal output with colors and formatting
- **openai**: AI integration for code generation
- **python-dotenv**: Environment variable management
- Additional supporting libraries (see requirements.txt)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Made with ❤️ by [Sumanta Kabiraj](https://github.com/infysumanta)
