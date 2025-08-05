import sys

def graceful_exit(message="Goodbye! Application terminated gracefully."):
    """Handle graceful application termination with consistent messaging."""
    print(f"\n\n{message}")
    sys.exit(0)

def handle_keyboard_interrupt():
    """Handle KeyboardInterrupt (Ctrl+C) gracefully."""
    graceful_exit()

def handle_eof_error():
    """Handle EOFError (Ctrl+D on Unix, Ctrl+Z on Windows) gracefully."""
    graceful_exit() 