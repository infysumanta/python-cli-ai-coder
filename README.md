# Code Project Generator

A Python tool that uses OpenAI's GPT-4o to generate complete project structures based on user specifications.

## Project Structure

The project has been organized with a proper folder structure:

```
code-project-generator/
├── .env                  # Environment variables (contains OpenAI API key)
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

## Features

- Generate complete project structures for various types of projects (MERN, Django+React, etc.)
- Create appropriate directory structures and files with proper content
- Generate README.md files for projects
- Track and summarize project generation process

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd code-project-generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the project generator:

```
python main.py
```

Follow the prompts to specify:
- Project type (e.g., MERN Stack, Django+React)
- Project name
- Project description

The tool will generate a complete project structure based on your specifications.

## Dependencies

- openai: For GPT-4o API access
- python-dotenv: For loading environment variables
- Other supporting libraries (see requirements.txt)

## License

[Specify license information here]
