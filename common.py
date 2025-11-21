from PIL import ImageGrab
import numpy as np
import platform
import subprocess

# Global variable to track current brightness for smooth transitions
current_brightness = None


def average_light_level(min_brightness=0, max_brightness=100, smooth_transitions=True, verbose=True):
    screen_image = ImageGrab.grab()

    image = screen_image.convert('L')
    width, height = image.size
    part_width = width // 8
    part_height = height // 8

    # Calculate overall screen brightness directly
    image_array = np.array(image)
    detected_level = np.mean(image_array)

    if verbose:
        print(f"Screen brightness level: {detected_level:.1f}")

    # Map detected level to user's brightness range
    # Screen brightness typically ranges from 0 (black) to 255 (white)
    min_detected = 0
    max_detected = 255

    # Clamp detected level to expected range
    clamped_level = max(min_detected, min(max_detected, detected_level))

    # Normalize to 0-1 based on detected range
    normalized_level = clamped_level / max_detected

    # Invert the mapping: dark screen (low detected_level) = high brightness
    # bright screen (high detected_level) = low brightness
    inverted_level = 1.0 - normalized_level
    mapped_brightness = min_brightness + (inverted_level * (max_brightness - min_brightness))

    target_brightness = max(min_brightness, min(max_brightness, int(mapped_brightness)))

    # Apply smooth transitions if enabled
    if not smooth_transitions:
        return target_brightness
    
    # Implement smooth transition with hysteresis to prevent rapid switching
    global current_brightness
    if current_brightness is None:
        current_brightness = target_brightness
        return target_brightness

    # Add hysteresis - only change if difference is significant enough
    hysteresis_threshold = 1
    diff = target_brightness - current_brightness

    if abs(diff) <= hysteresis_threshold:
        # Stay at current brightness if change is too small
        return int(current_brightness)

    # Calculate step size for smooth transition
    max_step = 2  # Maximum brightness change per update

    if abs(diff) <= max_step:
        current_brightness = target_brightness
    else:
        # Move towards target gradually
        step = max_step if diff > 0 else -max_step
        current_brightness += step

    return int(current_brightness)
def detect_os():
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        return "Linux"
    elif system == "Darwin":
        return "macOS"
    else:
        return "Unknown"
