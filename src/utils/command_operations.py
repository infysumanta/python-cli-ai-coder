"""
Command execution functions.
"""
import os
import subprocess


def is_safe_command(command):
    """
    Checks if a command is safe to execute (no sudo).
    
    Args:
        command (str): Command to check
        
    Returns:
        bool: True if command is safe, False otherwise
    """
    # Check if command contains sudo
    if "sudo" in command.lower().split():
        return False
    return True


def run_command(command):
    """
    Runs a terminal command in the current working directory, without sudo.
    
    Args:
        command (str): Command to run
        
    Returns:
        dict: Dictionary with 'stdout', 'stderr', and 'returncode' if successful
        None: If command contains sudo or other error occurs
    """
    if not is_safe_command(command):
        print("Error: Cannot run commands with 'sudo'.")
        return None
    
    try:
        # Run the command and capture output
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()  # Ensure command runs in current working directory
        )
        
        # Get output
        stdout, stderr = process.communicate()
        
        return {
            'stdout': stdout,
            'stderr': stderr,
            'returncode': process.returncode
        }
    except Exception as e:
        print(f"Error running command: {e}")
        return None
