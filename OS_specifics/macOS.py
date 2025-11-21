from common import average_light_level
import subprocess

def set_brightness(brightness):
    set_brightness = f'brightness {brightness/100}'
    subprocess.run(set_brightness, shell=True)

def check_macOS(min_brightness, max_brightness, smooth_transitions=True, verbose=True):
    target_brightness = average_light_level(min_brightness, max_brightness, smooth_transitions, verbose)
    set_brightness(target_brightness)
    
    if verbose:
        print("Target brightness level:", target_brightness)
