import sys
import signal
from client.menus.main_menu import show_main_menu

def signal_handler(sig, frame):
    print("\n\nGoodbye! Application terminated gracefully.")
    sys.exit(0)

def main():
    # Set up signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        show_main_menu()
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Application terminated.")
        sys.exit(1)

if __name__ == "__main__":
    main()