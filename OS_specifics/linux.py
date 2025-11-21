from common import average_light_level
import subprocess

_primary_display = None

def get_primary_display():
    """Get the primary display name for xrandr, cached for performance"""
    global _primary_display
    if _primary_display is not None:
        return _primary_display
        
    try:
        result = subprocess.run(['xrandr', '--query'], 
                              capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if ' connected primary' in line:
                _primary_display = line.split()[0]
                return _primary_display
        # If no primary found, get first connected display
        for line in lines:
            if ' connected' in line and 'disconnected' not in line:
                _primary_display = line.split()[0]
                return _primary_display
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Fallback to common display names
    common_displays = ['eDP-1', 'LVDS-1', 'DP-1', 'HDMI-1', 'VGA-1']
    for display in common_displays:
        try:
            subprocess.run(['xrandr', '--output', display, '--brightness', '1.0'], 
                         capture_output=True, check=True)
            _primary_display = display
            return _primary_display
        except subprocess.CalledProcessError:
            continue
    
    _primary_display = None
    return None

def set_brightness(brightness):
    """Set brightness using xrandr overlay (0-100% maps to 0.1-1.0)"""
    # Convert percentage to xrandr brightness value (0.1 to 1.0)
    # Minimum of 0.1 to prevent completely black screen
    xrandr_brightness = max(0.1, min(1.0, brightness / 100.0))
    
    display = get_primary_display()
    if not display:
        print("Error: Could not detect display for xrandr")
        return
    
    try:
        subprocess.run(['xrandr', '--output', display, '--brightness', str(xrandr_brightness)],
                      check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error setting brightness with xrandr: {e}")

def check_linux(min_brightness, max_brightness, smooth_transitions=True, verbose=True):
    # Ensure the display is cached
    get_primary_display()
    
    target_brightness = average_light_level(min_brightness, max_brightness, smooth_transitions, verbose)
    set_brightness(target_brightness)

    if verbose:
        print("Target brightness level:", target_brightness)
