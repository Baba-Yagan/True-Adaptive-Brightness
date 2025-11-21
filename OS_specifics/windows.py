from common import average_light_level
import wmi
import win32gui
import win32con
import win32process
import time


# Connect to WMI
c = wmi.WMI(namespace='wmi')

# Get brightness
def get_brightness():
    brightness = c.WmiMonitorBrightness()[0].CurrentBrightness
    return brightness
def set_brightness(brightness):
    brightness = min(max(brightness, 0), 100)
    c.WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)  



def check_windows(min_brightness, max_brightness, smooth_transitions=True, verbose=True):
    try:
        target_brightness = average_light_level(min_brightness, max_brightness, smooth_transitions, verbose)
    except OSError as e:
        print(f"Error capturing screen: {e}. Retrying in 5 seconds...")
        time.sleep(5)
        check_windows(min_brightness, max_brightness, smooth_transitions, verbose)
        return
    
    current_brightness = get_brightness()
    
    # Only adjust if there's a significant difference (avoid constant small adjustments)
    if abs(current_brightness - target_brightness) > 5:
        set_brightness(target_brightness)
        if verbose:
            print(f"Brightness adjusted from {current_brightness}% to {target_brightness}%")
    
    if verbose:
        print("Target brightness level:", target_brightness)
    
