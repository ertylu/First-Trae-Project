import pyautogui
import math
import time

# Give user time to position mouse over the drawing area
print("You have 5 seconds to position your mouse over the drawing area...")
time.sleep(5)

# Define circle parameters
center_x, center_y = pyautogui.position()  # Use current mouse position as center
radius = 100  # Radius in pixels
num_points = 128  # Number of points to draw (more points = smoother circle)

# Calculate the first point on the circle
start_x = center_x + radius
start_y = center_y

# Move to the starting point
pyautogui.moveTo(start_x, start_y)

# Press the mouse button down
pyautogui.mouseDown()

# Draw the circle by moving through calculated points
try:
    for i in range(num_points + 1):  # +1 to complete the circle
        angle = math.radians(i * (360 / num_points))
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # Move to the next point on the circle
        pyautogui.moveTo(x, y)
        
        # Small delay to control drawing speed
        time.sleep(0.02)
        
    # Alternative method using dragTo (uncomment to use)
    # for i in range(num_points + 1):
    #     angle = math.radians(i * (360 / num_points))
    #     x = center_x + radius * math.cos(angle)
    #     y = center_y + radius * math.sin(angle)
    #     pyautogui.dragTo(x, y, duration=0.1)
        
finally:
    # Always release the mouse button when done or if an error occurs
    pyautogui.mouseUp()
    print("Circle drawing completed!")
pyautogui.displayMousePosition()