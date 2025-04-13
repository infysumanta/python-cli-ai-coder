"""
Command-line interface for the project generator.
"""
import os
import json
import time
import shutil
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table
from rich.markdown import Markdown
from rich.text import Text
from rich.style import Style
from rich.live import Live
from rich.layout import Layout
from rich.columns import Columns

from src.core.project_generator import ProjectGenerator


# Initialize Rich console
console = Console()

# Define project type options with icons
PROJECT_TYPES = {
    1: {
        "name": "Python",
        "icon": "🐍"  # Snake emoji for Python
    },
    2: {
        "name": "JavaScript",
        "icon": "🐛"  # JS bug emoji
    },
    3: {
        "name": "TypeScript",
        "icon": "🔥"  # Fire emoji for TypeScript
    },
    4: {
        "name": "React + Vite + TypeScript",
        "icon": "⚛️"  # Atom symbol for React
    },
    5: {
        "name": "React + Vite + JavaScript",
        "icon": "⚛️"  # Atom symbol for React
    },
    6: {
        "name": "Express + TypeScript",
        "icon": "🚀"  # Rocket emoji for Express
    },
    7: {
        "name": "Express + JavaScript",
        "icon": "🚀"  # Rocket emoji for Express
    },
    8: {
        "name": "Custom (specify)",
        "icon": "⚙️"  # Gear emoji for custom
    }
}

# Define project features with icons
PROJECT_FEATURES = {
    "git": {
        "name": "Git Initialization",
        "description": "Initialize a Git repository with .gitignore",
        "default": True,
        "exclude_message": "No Git initialization or .gitignore files",
        "icon": "🔀"  # Git branch symbol
    },
    "tests": {
        "name": "Testing Framework",
        "description": "Add testing framework and sample tests",
        "default": True,
        "exclude_message": "No testing framework or test files",
        "icon": "🚨"  # Test/alert symbol
    },
    "github_actions": {
        "name": "GitHub Actions",
        "description": "Add CI/CD workflows with GitHub Actions",
        "default": False,
        "exclude_message": "No GitHub Actions or CI/CD workflows",
        "icon": "🛠️"  # Hammer and wrench for CI/CD
    },
    "docs": {
        "name": "Documentation",
        "description": "Add documentation structure and templates",
        "default": False,
        "exclude_message": "No documentation beyond basic README.md",
        "icon": "📝"  # Documentation symbol
    }
}


def main():
    """
    Main function that takes input from the terminal and runs the generator.
    """
    # Display a simpler header
    console.print("\n[bold cyan]GPT-4o PROJECT GENERATOR[/bold cyan]")
    console.print("[dim]Create complete project structures with AI[/dim]")
    console.print("\n[yellow]Please provide the following information:[/yellow]")

    # Display project type options in a table with icons
    console.print("\n[bold magenta]Available Project Types:[/bold magenta]")

    # Create a table with icons
    type_table = Table(show_header=False, box=None)
    type_table.add_column("Number", style="cyan", justify="right")
    type_table.add_column("Icon", justify="center")
    type_table.add_column("Project Type", style="green")

    for key, value in PROJECT_TYPES.items():
        type_table.add_row(
            f"[bold cyan]{key}[/bold cyan]",
            value["icon"],
            f"[green]{value['name']}[/green]"
        )

    console.print(type_table)

    # Get project type selection
    type_choice = IntPrompt.ask(
        "\n[bold green]Select project type[/bold green] [dim](enter number)[/dim]",
        choices=[str(i) for i in PROJECT_TYPES.keys()],
        show_choices=False
    )

    # Handle custom project type
    if type_choice == 8:  # Custom option
        project_type = Prompt.ask(
            "[bold green]Enter custom project type[/bold green]"
        ).strip()
    else:
        project_type = PROJECT_TYPES[type_choice]["name"]

    # Get project name with Rich prompt
    project_name = Prompt.ask("[bold green]Enter project name[/bold green]").strip()

    # Convert project name to a valid folder name for suggestion only
    suggested_folder_name = project_name.lower().replace(" ", "_")

    # Create a default project path in the 'projects' directory
    default_project_path = os.path.join("projects", suggested_folder_name)

    # Ask for project directory path
    project_folder = Prompt.ask(
        "[bold green]Project directory[/bold green] [dim](where to store the project)[/dim]",
        default=default_project_path
    ).strip()

    # Extract the project folder name from the path
    project_folder_name = os.path.basename(project_folder)

    # Show the full path that will be created
    console.print(f"[dim]Project will be created at:[/dim] [cyan]{os.path.abspath(project_folder)}[/cyan]")

    # Create the project directory and any parent directories if they don't exist
    with console.status(f"[bold green]Creating directory {project_folder}...[/bold green]"):
        # Get the parent directory
        parent_dir = os.path.dirname(project_folder)

        # Create parent directory first if it doesn't exist and it's not the current directory
        if parent_dir and not os.path.exists(parent_dir):
            console.print(f"[dim]Creating parent directory: {parent_dir}[/dim]")
            os.makedirs(parent_dir, exist_ok=True)

        # Create the project directory
        if not os.path.exists(project_folder):
            os.makedirs(project_folder, exist_ok=True)

    # Get project description as a single input with prompt
    console.print("\n[bold green]Enter project description:[/bold green]")
    project_description = Prompt.ask(
        "[dim]Describe your project[/dim]",
        console=console
    )

    # Show the description in a panel
    if project_description:
        console.print(Panel(
            f"[yellow]{project_description}[/yellow]",
            title="[bold]Description[/bold]",
            border_style="green"
        ))

    # Create an empty list to maintain compatibility
    project_description_lines = [project_description]

    project_description = "\n".join(project_description_lines)

    # Get the OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        console.print(Panel.fit(
            "[bold red]Error: OPENAI_API_KEY not found in environment variables.[/bold red]\n" +
            "Please set this variable in a .env file or directly in your environment.",
            title="[white on red] API Key Missing [/white on red]",
            border_style="red"
        ))
        return

    # Save the original directory
    original_dir = os.getcwd()

    # Change to the project directory if it's not the current directory
    if os.path.abspath(original_dir) != os.path.abspath(project_folder):
        console.print(f"[dim]Changing to project directory: {project_folder}[/dim]")
        os.chdir(project_folder)

    # Create the project generator
    generator = ProjectGenerator(api_key)

    # Get project features
    console.print("\n[bold magenta]Select Project Features[/bold magenta]")

    # Create an enhanced feature selection display with icons
    console.print("\n[bold magenta]Project Features:[/bold magenta]")

    # Create a table for features
    feature_table = Table(show_header=False, box=None)
    feature_table.add_column("Icon", justify="center")
    feature_table.add_column("Feature", style="green")
    feature_table.add_column("Description", style="cyan")
    feature_table.add_column("Default", justify="center")

    # Add rows for each feature
    selected_features = {}
    for key, feature in PROJECT_FEATURES.items():
        # Pre-select based on defaults
        selected_features[key] = feature["default"]

        # Create status indicator
        status_icon = "[green]✓[/green]" if feature["default"] else "[yellow]✗[/yellow]"

        # Add row to table
        feature_table.add_row(
            feature["icon"],
            f"[bold green]{feature['name']}[/bold green]",
            feature["description"],
            status_icon
        )

    console.print(feature_table)

    # Ask for each feature with icons
    for key, feature in PROJECT_FEATURES.items():
        selected_features[key] = Confirm.ask(
            f"\n{feature['icon']} [bold green]Include {feature['name']}?[/bold green]\n" +
            f"[dim]If disabled: {feature['exclude_message']}[/dim]",
            default=feature["default"]
        )

        # Show immediate feedback
        if selected_features[key]:
            console.print(f"  {feature['icon']} [green]✓ {feature['name']} will be included[/green]")
        else:
            console.print(f"  {feature['icon']} [yellow]✗ {feature['name']} will be excluded[/yellow]")

    # Show project details in a simpler format
    console.print("\n[bold cyan]Project Summary:[/bold cyan]")
    console.print(f"[bold]Name:[/bold] [green]{project_name}[/green]")
    console.print(f"[bold]Type:[/bold] [green]{project_type}[/green]")
    console.print(f"[bold]Directory:[/bold] [green]{project_folder}[/green]")

    # Show selected features with icons
    console.print("\n[bold cyan]Selected Features:[/bold cyan]")

    # Create a table for selected features
    selected_table = Table(show_header=False, box=None)
    selected_table.add_column("Status", justify="center")
    selected_table.add_column("Icon", justify="center")
    selected_table.add_column("Feature", style="green")

    for k, v in selected_features.items():
        if v:
            selected_table.add_row(
                "[bold green]✓[/bold green]",
                PROJECT_FEATURES[k]['icon'],
                f"[green]{PROJECT_FEATURES[k]['name']}[/green]"
            )
        else:
            selected_table.add_row(
                "[bold yellow]✗[/bold yellow]",
                PROJECT_FEATURES[k]['icon'],
                f"[yellow]{PROJECT_FEATURES[k]['name']} - {PROJECT_FEATURES[k]['exclude_message']}[/yellow]"
            )

    console.print(selected_table)

    # Confirm before proceeding
    if not Confirm.ask("\n[yellow]Ready to generate your project?[/yellow]"):
        console.print("[italic]Project generation cancelled.[/italic]")
        os.chdir(original_dir)  # Return to original directory
        return

    # Show a spinner while initializing
    with console.status("[bold green]Initializing project generation...[/bold green]"):
        time.sleep(1.5)  # Brief pause for effect

    # Create an enhanced progress display for the generation process
    console.print("\n[bold cyan]Generating Project...[/bold cyan]")

    progress_display = Progress(
        SpinnerColumn('dots'),
        TextColumn("[bold cyan]Generating project structure...[/bold cyan]"),
        BarColumn(bar_width=40, complete_style="green", finished_style="green"),
        TextColumn("[yellow]{task.percentage:>3.0f}%[/yellow]"),
        TimeRemainingColumn(),
        console=console,
        expand=True,
        transient=False  # Keep progress history visible
    )

    # Create a task for overall progress
    with progress_display as progress:
        # Create a task for overall progress
        overall_task = progress.add_task("Generating", total=100)

        # Last status message
        last_status = ""
        last_percentage = 0

        # Custom wrapper to capture progress updates
        def progress_callback(step, total_steps, message):
            nonlocal last_status, last_percentage

            # Calculate percentage
            percentage = int((step/total_steps) * 100)

            # Update the progress bar
            progress.update(overall_task, completed=percentage)

            # Only update the description if the message has changed
            if message != last_status:
                # Add emoji based on the type of operation
                emoji = ""
                action_verb = ""

                if "file" in message.lower():
                    if "created file" in message.lower():
                        emoji = "✓"
                        action_verb = "Created file"
                        file_path = message.lower().replace("created file", "").strip()
                        # Print the file creation message below the progress bar
                        console.print(f"{emoji} [green]{action_verb}[/green] [cyan]{file_path}[/cyan]")
                elif "directory" in message.lower():
                    if "created directory" in message.lower():
                        emoji = "✓"
                        action_verb = "Created directory"
                        dir_path = message.lower().replace("created directory", "").strip()
                        # Print the directory creation message below the progress bar
                        console.print(f"{emoji} [green]{action_verb}[/green] [cyan]{dir_path}[/cyan]")
                elif "complete" in message.lower():
                    emoji = "✅"
                    # Print completion message
                    console.print(f"{emoji} [bold green]{message}[/bold green]")

                # Update last status
                last_status = message
                last_percentage = percentage

        # Generate the complete project with progress tracking
        result = generator.generate_project(
            project_type,
            project_name,
            project_description,
            progress_callback,
            selected_features
        )

    # Show completion message
    console.print("\n[bold green]✅ PROJECT GENERATION COMPLETE[/bold green]")

    # Show basic statistics
    console.print("\n[bold cyan]Generation Statistics:[/bold cyan]")
    console.print(f"[bold]Project:[/bold] [green]{result['project_name']}[/green]")
    console.print(f"[bold]Directory:[/bold] [green]{project_folder}[/green]")
    console.print(f"[bold]Time:[/bold] [green]{result['generation_time_seconds']:.2f} seconds[/green]")
    console.print(f"[bold]Files:[/bold] [green]{result['total_files']}[/green]")
    console.print(f"[bold]Directories:[/bold] [green]{result['total_directories']}[/green]")

    # Show feature information if available with icons
    if 'features' in result and result['features']:
        console.print("\n[bold cyan]Features:[/bold cyan]")

        # Create a table for features
        feature_result_table = Table(show_header=False, box=None)
        feature_result_table.add_column("Status", justify="center")
        feature_result_table.add_column("Icon", justify="center")
        feature_result_table.add_column("Feature", style="green")

        for feature_key, enabled in result['features'].items():
            feature_name = PROJECT_FEATURES[feature_key]['name']
            feature_icon = PROJECT_FEATURES[feature_key]['icon']

            if enabled:
                feature_result_table.add_row(
                    "[bold green]✓[/bold green]",
                    feature_icon,
                    f"[green]{feature_name}[/green]"
                )
            else:
                feature_result_table.add_row(
                    "[bold yellow]✗[/bold yellow]",
                    feature_icon,
                    f"[yellow]{feature_name}[/yellow]"
                )

        console.print(feature_result_table)

    # Show a summary of created files and directories
    console.print("\n[bold cyan]Project Structure:[/bold cyan]")

    # Show directories in a table
    if result['directories_created']:
        console.print("[bold blue]Directories:[/bold blue]")

        # Create a table for directories
        dir_table = Table(show_header=False, box=None)
        dir_table.add_column("Icon", justify="center")
        dir_table.add_column("Directory", style="blue")

        for directory in result['directories_created'][:5]:  # Show only first 5
            dir_table.add_row("📁", f"[blue]{directory}[/blue]")

        console.print(dir_table)

        if len(result['directories_created']) > 5:
            console.print(f"[blue]… and {len(result['directories_created']) - 5} more directories[/blue]")

    # Show files in a table
    if result['files_created']:
        console.print("\n[bold yellow]Files:[/bold yellow]")

        # Create a table for files
        file_table = Table(show_header=False, box=None)
        file_table.add_column("Icon", justify="center")
        file_table.add_column("File", style="yellow")

        for file in result['files_created'][:5]:  # Show only first 5
            file_table.add_row("📄", f"[yellow]{file}[/yellow]")

        console.print(file_table)

        if len(result['files_created']) > 5:
            console.print(f"[yellow]… and {len(result['files_created']) - 5} more files[/yellow]")

    # Display a simplified summary
    console.print("\n[bold green]Project Summary:[/bold green]")
    # Extract first 300 characters of summary
    summary_preview = result['summary'][:300] + ("..." if len(result['summary']) > 300 else "")
    console.print(f"[green]{summary_preview}[/green]")

    # Save the project summary to a file with a spinner
    summary_filename = f"{project_name}_generation_summary.json"
    summary_filepath = os.path.join(project_folder, summary_filename)
    with console.status(f"[bold]Saving generation summary to file...[/bold]"):
        with open(summary_filepath, "w") as f:
            json.dump(result, f, indent=2)
        time.sleep(0.5)  # Brief pause for effect

    console.print(f"\n[bold green]✓[/bold green] Detailed generation summary saved to [bold cyan]{summary_filepath}[/bold cyan]")

    # Final success message
    console.print(f"\n[bold green]Your project [bold cyan]{project_name}[/bold cyan] has been successfully generated![/bold green]")
    console.print("[italic]Happy coding![/italic]")

    # Ask if user wants to add features to the project
    if Confirm.ask("\n[yellow]Would you like to add features to this project?[/yellow]"):
        add_features_to_project(generator, project_name, project_type, project_folder, result)
    else:
        console.print("[italic]Returning to original directory...[/italic]")
        # Return to original directory if we're not already there
        original_dir = os.getcwd()
        if original_dir != os.path.dirname(os.path.abspath(project_folder)):
            os.chdir(original_dir)


def add_features_to_project(generator, project_name, project_type, project_folder, project_info):
    """
    Add new features to an existing project.
    """
    console.print("\n[bold cyan]ADD FEATURES TO PROJECT[/bold cyan]")
    console.print("[dim]Enhance your project with new functionality[/dim]")

    # Get feature description as a single input with prompt
    console.print("\n[bold green]Describe the feature you want to add:[/bold green]")
    feature_description = Prompt.ask(
        "[dim]Describe your feature[/dim]",
        console=console
    )

    # Show the description in a panel
    if feature_description:
        console.print(Panel(
            f"[yellow]{feature_description}[/yellow]",
            title="[bold]Feature Description[/bold]",
            border_style="green"
        ))

    # Create an empty list to maintain compatibility
    feature_description_lines = [feature_description]

    feature_description = "\n".join(feature_description_lines)

    # Show feature details in a simpler format
    console.print("\n[bold cyan]Feature Details:[/bold cyan]")
    console.print(f"[bold]Project:[/bold] [green]{project_name}[/green]")
    console.print(f"[bold]Directory:[/bold] [green]{project_folder}[/green]")
    console.print(f"[bold]Feature:[/bold] [green]{feature_description}[/green]")

    # Confirm before proceeding
    if not Confirm.ask("\n[yellow]Ready to add this feature?[/yellow]"):
        console.print("[italic]Feature addition cancelled.[/italic]")
        return

    # Create a progress display for the feature addition process
    with console.status("[bold green]Analyzing project structure...[/bold green]"):
        time.sleep(1.5)  # Brief pause for effect

    # Create an enhanced progress display for the feature addition process
    console.print("\n[bold cyan]Adding Feature...[/bold cyan]")

    progress_display = Progress(
        SpinnerColumn('dots'),
        TextColumn("[bold cyan]Adding feature to project...[/bold cyan]"),
        BarColumn(bar_width=40, complete_style="green", finished_style="green"),
        TextColumn("[yellow]{task.percentage:>3.0f}%[/yellow]"),
        TimeRemainingColumn(),
        console=console,
        expand=True,
        transient=False  # Keep progress history visible
    )

    # Create a task for overall progress
    with progress_display as progress:
        # Create a task for overall progress
        overall_task = progress.add_task("Adding feature", total=100)

        # Last status message
        last_status = ""
        last_percentage = 0

        # Custom wrapper to capture progress updates
        def progress_callback(step, total_steps, message):
            nonlocal last_status, last_percentage

            # Calculate percentage
            percentage = int((step/total_steps) * 100)

            # Update the progress bar
            progress.update(overall_task, completed=percentage)

            # Only update the description if the message has changed
            if message != last_status:
                # Add emoji based on the type of operation
                emoji = ""
                action_verb = ""

                if "file" in message.lower():
                    if "created file" in message.lower():
                        emoji = "✓"
                        action_verb = "Created file"
                        file_path = message.lower().replace("created file", "").strip()
                        # Print the file creation message below the progress bar
                        console.print(f"{emoji} [green]{action_verb}[/green] [cyan]{file_path}[/cyan]")
                    elif "modified file" in message.lower():
                        emoji = "✏️"
                        action_verb = "Modified file"
                        file_path = message.lower().replace("modified file", "").strip()
                        # Print the file modification message below the progress bar
                        console.print(f"{emoji} [green]{action_verb}[/green] [cyan]{file_path}[/cyan]")
                elif "directory" in message.lower():
                    if "created directory" in message.lower():
                        emoji = "✓"
                        action_verb = "Created directory"
                        dir_path = message.lower().replace("created directory", "").strip()
                        # Print the directory creation message below the progress bar
                        console.print(f"{emoji} [green]{action_verb}[/green] [cyan]{dir_path}[/cyan]")
                elif "analyzing" in message.lower():
                    emoji = "🔍"
                    # Print analyzing message
                    console.print(f"{emoji} [blue]{message}[/blue]")
                elif "complete" in message.lower():
                    emoji = "✅"
                    # Print completion message
                    console.print(f"{emoji} [bold green]{message}[/bold green]")

                # Update last status
                last_status = message
                last_percentage = percentage

        # Add the feature to the project with progress tracking
        result = generator.add_feature_to_project(project_type, project_name, feature_description, project_info, progress_callback)

    # Show feature addition summary
    console.print("\n[bold green]✅ FEATURE ADDITION COMPLETE[/bold green]")

    # Display a simplified summary
    if result and 'summary' in result:
        console.print("\n[bold cyan]Feature Summary:[/bold cyan]")
        # Extract first 300 characters of summary
        summary_preview = result['summary'][:300] + ("..." if len(result['summary']) > 300 else "")
        console.print(f"[green]{summary_preview}[/green]")

    # Ask if user wants to add more features
    if Confirm.ask("\n[yellow]Would you like to add more features?[/yellow]"):
        add_features_to_project(generator, project_name, project_type, project_folder, project_info)
    else:
        # Return to original directory
        console.print(f"[italic]Returning to original directory...[/italic]")
        # Get the original directory (the one we were in before entering the project folder)
        original_dir = os.getcwd()
        if original_dir != os.path.dirname(os.path.abspath(project_folder)):
            os.chdir(original_dir)
