import platform
import time
import sys
from common import detect_os

def parse_arguments():
    """Parse command line arguments"""
    if len(sys.argv) < 4:
        print("Usage: python main.py <smooth> <min_brightness> <max_brightness> [verbose]")
        print("  smooth: 'true' or 'false'")
        print("  min_brightness: 0-100")
        print("  max_brightness: 0-100")
        print("  verbose: 'true' or 'false' (optional, default: 'true')")
        sys.exit(1)
    
    smooth = sys.argv[1].lower()
    if smooth not in ['true', 'false']:
        print("Error: smooth must be 'true' or 'false'")
        sys.exit(1)
    smooth_transitions = smooth == 'true'
    
    try:
        min_brightness = int(sys.argv[2])
        max_brightness = int(sys.argv[3])
    except ValueError:
        print("Error: brightness values must be integers")
        sys.exit(1)
    
    # Parse optional verbose flag
    verbose = True  # Default to true for backward compatibility
    if len(sys.argv) >= 5:
        verbose_arg = sys.argv[4].lower()
        if verbose_arg not in ['true', 'false']:
            print("Error: verbose must be 'true' or 'false'")
            sys.exit(1)
        verbose = verbose_arg == 'true'
    
    if not (0 <= min_brightness <= 100):
        print("Error: min_brightness must be between 0 and 100")
        sys.exit(1)
    
    if not (0 <= max_brightness <= 100):
        print("Error: max_brightness must be between 0 and 100")
        sys.exit(1)
    
    if min_brightness > max_brightness:
        print("Error: min_brightness cannot be greater than max_brightness")
        sys.exit(1)
    
    return smooth_transitions, min_brightness, max_brightness, verbose

time_delay = 0.5  # Balanced delay for smooth but not too rapid updates
os_name = detect_os()
print("Operating System:", os_name)

# Parse command line arguments
smooth_transitions, min_brightness, max_brightness, verbose = parse_arguments()
print(f"Using hardware brightness control")
print(f"Smooth transitions: {'enabled' if smooth_transitions else 'disabled'}")
print(f"Brightness range set: {min_brightness}% - {max_brightness}%")
print(f"Verbose output: {'enabled' if verbose else 'disabled'}")

# Hardware brightness control
if(os_name == "Windows"):
    from OS_specifics.windows import check_windows
    while True:
        check_windows(min_brightness, max_brightness, smooth_transitions, verbose)
        time.sleep(time_delay)
elif( os_name == "Linux"):
    from OS_specifics.linux import check_linux
    while True:
        check_linux(min_brightness, max_brightness, smooth_transitions, verbose)
        time.sleep(time_delay)
elif( os_name == "macOS"):
    from OS_specifics.macOS import check_macOS
    while True:
        check_macOS(min_brightness, max_brightness, smooth_transitions, verbose)
        time.sleep(time_delay)
