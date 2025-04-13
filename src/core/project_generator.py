"""
Project generator core functionality.
"""
import os
import json
import time
import datetime
from pathlib import Path
from openai import OpenAI

from src.utils.file_operations import (
    read_file, get_file_metadata, list_directory_contents,
    write_to_file, create_directory
)
from src.utils.command_operations import run_command


class ProjectGenerator:
    def __init__(self, api_key):
        """
        Initializes the project generator with OpenAI API key.

        Args:
            api_key (str): OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
        self.available_tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Reads contents of a file in the current working directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "Name of the file to read"
                            }
                        },
                        "required": ["filename"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_file_metadata",
                    "description": "Returns metadata for a file in the current working directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "Name of the file to get metadata for"
                            }
                        },
                        "required": ["filename"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory_contents",
                    "description": "Lists all files and directories in the specified directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directory to list contents from (defaults to current directory)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_to_file",
                    "description": "Writes content to a file in the current working directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "Name of the file to write to"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write to the file"
                            },
                            "mode": {
                                "type": "string",
                                "description": "Write mode ('w' for overwrite, 'a' for append)",
                                "enum": ["w", "a"]
                            }
                        },
                        "required": ["filename", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_command",
                    "description": "Runs a terminal command in the current working directory, without sudo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Command to run"
                            }
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_directory",
                    "description": "Creates a directory in the current working directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory_name": {
                                "type": "string",
                                "description": "Name of directory to create"
                            }
                        },
                        "required": ["directory_name"]
                    }
                }
            }
        ]
        self.messages = []
        self.project_name = None

    def generate_readme(self, project_type, project_name, project_description, project_structure=None):
        """
        Generates or regenerates a README.md file for a project.

        Args:
            project_type (str): Type of the project (e.g., "MERN", "Django+React", etc.)
            project_name (str): Name of the project
            project_description (str): Detailed description of the project
            project_structure (dict, optional): Existing project structure information

        Returns:
            dict: Result of README generation
        """
        start_time = time.time()

        # Check if README.md already exists
        readme_exists = os.path.exists("README.md")

        # Initial prompt to GPT-4o
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert technical writer specialized in creating comprehensive README.md files "
                    "for software projects. Your task is to generate a professional README.md that follows "
                    "best practices and includes all standard sections such as project description, features, "
                    "installation, usage, API documentation (if applicable), technologies used, and contributing guidelines."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Generate a detailed README.md for a {project_type} project named '{project_name}' "
                    f"with the following description:\n\n{project_description}\n\n"
                    f"Use proper Markdown formatting and follow industry best practices for "
                    f"structuring a README file. Include sections for prerequisites, installation, "
                    f"usage, API endpoints (if applicable), and contributing guidelines."
                )
            }
        ]

        # If we have project structure info, add it to the prompt
        if project_structure:
            dir_list = "\n".join([f"- {d}" for d in project_structure.get("directories_created", [])])
            file_list = "\n".join([f"- {f}" for f in project_structure.get("files_created", [])])

            structure_prompt = (
                f"\n\nThis project has the following structure:\n\nDirectories:\n{dir_list}\n\n"
                f"Files:\n{file_list}\n\nPlease incorporate this structure information into "
                f"the README.md where appropriate, especially in the installation and usage sections."
            )

            messages[1]["content"] += structure_prompt

        try:
            # Get response from GPT-4o
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )

            # Get the README content
            readme_content = response.choices[0].message.content

            # Write to README.md
            success = write_to_file("README.md", readme_content)

            end_time = time.time()
            duration = end_time - start_time

            return {
                "success": success,
                "readme_existed": readme_exists,
                "content": readme_content,
                "generation_time_seconds": duration
            }

        except Exception as e:
            print(f"Error generating README: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _handle_tool_calls(self, tool_calls):
        """
        Handles tool calls from GPT-4o responses.

        Args:
            tool_calls (list): List of tool calls from the model

        Returns:
            list: List of tool responses
        """
        tool_responses = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            response_content = None

            if function_name == "read_file":
                response_content = read_file(function_args.get("filename"))

            elif function_name == "get_file_metadata":
                metadata = get_file_metadata(function_args.get("filename"))
                # Convert datetime objects to strings for JSON serialization
                if metadata:
                    for key, value in metadata.items():
                        if isinstance(value, datetime.datetime):
                            metadata[key] = value.isoformat()
                        elif isinstance(value, Path):
                            metadata[key] = str(value)
                response_content = metadata

            elif function_name == "list_directory_contents":
                response_content = list_directory_contents(function_args.get("directory", "."))

            elif function_name == "write_to_file":
                success = write_to_file(
                    function_args.get("filename"),
                    function_args.get("content"),
                    function_args.get("mode", "w")
                )
                response_content = {"success": success}

            elif function_name == "run_command":
                result = run_command(function_args.get("command"))
                response_content = result

            elif function_name == "create_directory":
                success = create_directory(function_args.get("directory_name"))
                response_content = {"success": success}

            tool_responses.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps(response_content)
            })

        return tool_responses

    def generate_project(self, project_type, project_name, project_description, progress_callback=None, selected_features=None):
        """
        Generates a fullstack project based on the provided specifications.

        Args:
            project_type (str): Type of the project (e.g., "MERN", "Django+React", etc.)
            project_name (str): Name of the project
            project_description (str): Detailed description of the project
            progress_callback (callable, optional): Callback function to report progress
            selected_features (dict, optional): Dictionary of selected project features

        Returns:
            dict: Project generation summary
        """
        self.project_name = project_name
        start_time = time.time()

        # Process selected features
        features_str = ""
        if selected_features:
            include_list = []
            exclude_list = []

            # Process each feature
            if selected_features.get("git", False):
                include_list.append("Git initialization with appropriate .gitignore")
            else:
                exclude_list.append("Do NOT initialize Git or create any .gitignore files")

            if selected_features.get("tests", False):
                include_list.append("Testing framework with sample tests")
            else:
                exclude_list.append("Do NOT include any testing frameworks or test files")

            if selected_features.get("github_actions", False):
                include_list.append("GitHub Actions CI/CD workflows")
            else:
                exclude_list.append("Do NOT include any GitHub Actions or CI/CD workflow files")

            if selected_features.get("docs", False):
                include_list.append("Documentation structure and templates")
            else:
                exclude_list.append("Do NOT create documentation directories or files beyond a basic README.md")

            # Build the features string with both includes and excludes
            features_str = ""

            if include_list:
                features_str += "\n\nPlease include the following features:\n" + "\n".join([f"- {f}" for f in include_list])

            if exclude_list:
                features_str += "\n\nIMPORTANT - Explicitly exclude these features:\n" + "\n".join([f"- {f}" for f in exclude_list])

        # Initial prompt to GPT-4o
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert fullstack developer assistant capable of generating complete project structures. "
                    "You have access to tools that can create directories, write files, and run commands "
                    "to set up a complete project structure. "
                    "Focus on creating a well-organized, production-ready project structure with proper files and content. "
                    "You must work only within the current directory and cannot use sudo commands. "
                    "When creating files, include proper content that would be expected in a professional project. "
                    "Be systematic and thorough in your approach.\n\n"
                    "IMPORTANT: You are already in the project's root directory. DO NOT create a subdirectory with the same name "
                    "as the project. All files should be created directly in the current directory or in appropriate subdirectories "
                    "for organization (like 'src', 'tests', 'docs', etc.).\n\n"
                    "IMPORTANT: You must strictly adhere to the user's feature selections. If a feature is explicitly excluded, "
                    "you must NOT generate any files or directories related to that feature. For example, if Git is excluded, "
                    "do not create .gitignore files or initialize Git repositories. If testing is excluded, do not create test "
                    "directories or test files. Respect all feature inclusions and exclusions precisely."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Generate a complete {project_type} project named '{project_name}' with the following description: {project_description}\n\n"
                    f"IMPORTANT: You are already in the project directory. DO NOT create a subdirectory named '{project_name}' or similar. "
                    f"All files should be created directly in the current directory or in appropriate subdirectories for organization.\n\n"
                    f"Please create the directory structure, all necessary files with appropriate content, "
                    f"and include configuration files and code files. "
                    f"Work step by step to build a production-ready project structure.\n\n"
                    f"IMPORTANT: You must strictly follow the feature selections below. Only include the specified features "
                    f"and explicitly exclude any features marked for exclusion.{features_str}"
                )
            }
        ]

        # Track all actions taken
        actions_taken = []
        generated_files = []
        generated_dirs = []

        max_steps = 25  # Limit the number of steps to prevent infinite loops
        step = 0

        print(f"Starting project generation for {project_name}...")
        print(f"Type: {project_type}")
        print(f"Description: {project_description}")
        print("=" * 80)

        while step < max_steps:
            step += 1
            step_message = f"Step {step} of project generation process"
            print(f"\n{step_message}")

            # Call progress callback if provided
            if progress_callback:
                progress_callback(step, max_steps, "Processing...")

            try:
                # Get response from GPT-4o
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=self.messages,
                    tools=self.available_tools,
                    tool_choice="auto"
                )

                # Get the response message
                response_message = response.choices[0].message

                # Add the response to messages
                self.messages.append(response_message.model_dump())

                # Check if the response contains tool calls
                if response_message.tool_calls:
                    tool_call_message = f"Processing {len(response_message.tool_calls)} tool calls"
                    print(f"- {tool_call_message}")

                    # Update progress callback
                    if progress_callback:
                        progress_callback(step, max_steps, tool_call_message)

                    # Handle the tool calls
                    tool_responses = self._handle_tool_calls(response_message.tool_calls)

                    # Track actions
                    for tool_call, tool_response in zip(response_message.tool_calls, tool_responses):
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        if function_name == "create_directory":
                            dir_name = function_args.get("directory_name")
                            generated_dirs.append(dir_name)
                            print(f"  Created directory: {dir_name}")

                            # Update progress callback
                            if progress_callback:
                                progress_callback(step, max_steps, f"Created directory: {dir_name}")

                        elif function_name == "write_to_file":
                            filename = function_args.get("filename")
                            generated_files.append(filename)
                            print(f"  Created file: {filename}")

                            # Update progress callback
                            if progress_callback:
                                progress_callback(step, max_steps, f"Created file: {filename}")

                        actions_taken.append({
                            "step": step,
                            "action": function_name,
                            "args": function_args,
                            "result": json.loads(tool_response["output"])
                        })

                    # Add individual tool responses to messages
                    for tool_response in tool_responses:
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_response["tool_call_id"],
                            "content": tool_response["output"]
                        })
                else:
                    message_preview = f"Assistant message: {response_message.content[:100]}..."
                    print(f"- {message_preview}")

                    # Update progress callback
                    if progress_callback:
                        progress_callback(step, max_steps, "Processing assistant message")

                    # Check if the project generation is complete
                    if "project generation is complete" in response_message.content.lower() or "project structure is now complete" in response_message.content.lower():
                        completion_message = "Project generation marked as complete by the assistant"
                        print(f"\n{completion_message}")

                        # Update progress callback with completion
                        if progress_callback:
                            progress_callback(max_steps, max_steps, "Project generation complete!")

                        break

                    # Ask for the next step
                    self.messages.append({
                        "role": "user",
                        "content": "Please continue with the next steps to complete the project structure."
                    })

            except Exception as e:
                print(f"Error during project generation: {e}")
                actions_taken.append({
                    "step": step,
                    "error": str(e)
                })
                break

        # Get the final summary of the project
        self.messages.append({
            "role": "user",
            "content": "Provide a summary of what you've created including the project structure, files, and key features."
        })

        summary_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages
        )

        summary = summary_response.choices[0].message.content

        end_time = time.time()
        duration = end_time - start_time

        # Return the project generation summary
        # Add selected features to the result
        features_info = {}
        if selected_features:
            features_info = {
                "git": selected_features.get("git", False),
                "tests": selected_features.get("tests", False),
                "github_actions": selected_features.get("github_actions", False),
                "docs": selected_features.get("docs", False)
            }

        return {
            "project_name": project_name,
            "project_type": project_type,
            "total_steps": step,
            "total_files": len(generated_files),
            "total_directories": len(generated_dirs),
            "files_created": generated_files,
            "directories_created": generated_dirs,
            "generation_time_seconds": duration,
            "summary": summary,
            "features": features_info,
            "actions": actions_taken
        }

    def add_feature_to_project(self, project_type, project_name, feature_description, project_info, progress_callback=None):
        """
        Adds a new feature to an existing project.

        Args:
            project_type (str): Type of the project
            project_name (str): Name of the project
            feature_description (str): Description of the feature to add
            project_info (dict): Information about the existing project
            progress_callback (callable, optional): Callback function to report progress

        Returns:
            dict: Feature addition summary
        """
        start_time = time.time()

        # Get the existing project structure
        existing_files = project_info.get('files_created', [])
        existing_dirs = project_info.get('directories_created', [])

        # Create a formatted list of existing files and directories for the prompt
        file_list = "\n".join([f"- {f}" for f in existing_files])
        dir_list = "\n".join([f"- {d}" for d in existing_dirs])

        # Initial prompt to GPT-4o for feature addition
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert fullstack developer assistant capable of adding new features to existing projects. "
                    "You have access to tools that can read files, create directories, write files, and run commands. "
                    "Focus on understanding the existing project structure and making appropriate modifications to add the requested feature. "
                    "You must work only within the current directory and cannot use sudo commands. "
                    "Be systematic and thorough in your approach, making sure the new feature integrates well with the existing code.\n\n"
                    "IMPORTANT: You are already in the project's root directory. DO NOT create a subdirectory with the same name "
                    "as the project. All files should be created directly in the current directory or in appropriate subdirectories "
                    "for organization (like 'src', 'tests', 'docs', etc.)."
                )
            },
            {
                "role": "user",
                "content": (
                    f"I have an existing {project_type} project named '{project_name}' with the following structure:\n\n"
                    f"Directories:\n{dir_list}\n\n"
                    f"Files:\n{file_list}\n\n"
                    f"I want to add the following feature to this project: {feature_description}\n\n"
                    f"IMPORTANT: You are already in the project's root directory. DO NOT create a subdirectory named '{project_name}' or similar. "
                    f"All files should be created directly in the current directory or in appropriate subdirectories for organization.\n\n"
                    f"Please analyze the existing project structure, read necessary files to understand the codebase, "
                    f"and then make appropriate modifications to implement this feature. "
                    f"Work step by step, explaining your changes and why they're needed."
                )
            }
        ]

        # Track all actions taken
        actions_taken = []
        modified_files = []
        new_files = []
        new_dirs = []

        max_steps = 15  # Limit the number of steps
        step = 0

        print(f"\nStarting feature addition to {project_name}...")
        print(f"Feature: {feature_description}")
        print("=" * 80)

        while step < max_steps:
            step += 1
            step_message = f"Step {step} of feature addition process"
            print(f"\n{step_message}")

            # Call progress callback if provided
            if progress_callback:
                progress_callback(step, max_steps, "Processing...")

            try:
                # Get response from GPT-4o
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=self.messages,
                    tools=self.available_tools,
                    tool_choice="auto"
                )

                # Get the response message
                response_message = response.choices[0].message

                # Add the response to messages
                self.messages.append(response_message.model_dump())

                # Check if the response contains tool calls
                if response_message.tool_calls:
                    tool_call_message = f"Processing {len(response_message.tool_calls)} tool calls"
                    print(f"- {tool_call_message}")

                    # Update progress callback
                    if progress_callback:
                        progress_callback(step, max_steps, tool_call_message)

                    # Handle the tool calls
                    tool_responses = self._handle_tool_calls(response_message.tool_calls)

                    # Track actions
                    for tool_call, tool_response in zip(response_message.tool_calls, tool_responses):
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        if function_name == "create_directory":
                            dir_name = function_args.get("directory_name")
                            new_dirs.append(dir_name)
                            print(f"  Created directory: {dir_name}")

                            # Update progress callback
                            if progress_callback:
                                progress_callback(step, max_steps, f"Created directory: {dir_name}")

                        elif function_name == "write_to_file":
                            filename = function_args.get("filename")
                            mode = function_args.get("mode", "w")

                            # Check if this is a new file or modifying an existing one
                            if mode == "w" and filename not in existing_files:
                                new_files.append(filename)
                                print(f"  Created new file: {filename}")
                            else:
                                if filename not in modified_files:
                                    modified_files.append(filename)
                                print(f"  Modified file: {filename}")

                            # Update progress callback
                            if progress_callback:
                                action = "Created" if filename in new_files else "Modified"
                                progress_callback(step, max_steps, f"{action} file: {filename}")

                        elif function_name == "read_file":
                            filename = function_args.get("filename")
                            print(f"  Reading file: {filename}")

                            # Update progress callback
                            if progress_callback:
                                progress_callback(step, max_steps, f"Analyzing file: {filename}")

                        actions_taken.append({
                            "step": step,
                            "action": function_name,
                            "args": function_args,
                            "result": json.loads(tool_response["output"])
                        })

                    # Add individual tool responses to messages
                    for tool_response in tool_responses:
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_response["tool_call_id"],
                            "content": tool_response["output"]
                        })
                else:
                    message_preview = f"Assistant message: {response_message.content[:100]}..."
                    print(f"- {message_preview}")

                    # Update progress callback
                    if progress_callback:
                        progress_callback(step, max_steps, "Processing assistant message")

                    # Check if the feature addition is complete
                    if "feature implementation is complete" in response_message.content.lower() or "feature has been successfully added" in response_message.content.lower():
                        completion_message = "Feature addition marked as complete by the assistant"
                        print(f"\n{completion_message}")

                        # Update progress callback with completion
                        if progress_callback:
                            progress_callback(max_steps, max_steps, "Feature addition complete!")

                        break

                    # Ask for the next step
                    self.messages.append({
                        "role": "user",
                        "content": "Please continue with the next steps to complete the feature implementation."
                    })

            except Exception as e:
                print(f"Error during feature addition: {e}")
                actions_taken.append({
                    "step": step,
                    "error": str(e)
                })
                break

        # Get the final summary of the feature addition
        self.messages.append({
            "role": "user",
            "content": "Provide a summary of the feature you've added, including what files were modified or created and how the feature works."
        })

        summary_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages
        )

        summary = summary_response.choices[0].message.content

        end_time = time.time()
        duration = end_time - start_time

        # Return the feature addition summary
        return {
            "project_name": project_name,
            "project_type": project_type,
            "feature_description": feature_description,
            "total_steps": step,
            "total_new_files": len(new_files),
            "total_modified_files": len(modified_files),
            "total_new_directories": len(new_dirs),
            "new_files": new_files,
            "modified_files": modified_files,
            "new_directories": new_dirs,
            "feature_addition_time_seconds": duration,
            "summary": summary,
            "actions": actions_taken
        }
