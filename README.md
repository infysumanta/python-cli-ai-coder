# Python CLI AI Coder

A powerful command-line tool that leverages artificial intelligence to generate complete project structures, add new features to existing projects, and streamline your development workflow.

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

Follow the interactive prompts to:

1. Select a project type
2. Enter a project name
3. Choose a directory to store the project
4. Provide a project description
5. Select optional features (Git, Tests, GitHub Actions, Documentation)

The tool will generate a complete project structure based on your specifications.

### Add Features to an Existing Project

After generating a project, you can add new features:

1. Select "Yes" when asked if you want to add features
2. Describe the feature you want to add
3. The tool will analyze your project and implement the new feature

## ⚙️ Configuration Options

- **Project Types**: Choose from predefined templates or create custom ones
- **Project Features**:
  - **Git**: Initialize a Git repository with appropriate .gitignore
  - **Tests**: Add testing framework with sample tests
  - **GitHub Actions**: Set up CI/CD workflows
  - **Documentation**: Create documentation structure and templates

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
