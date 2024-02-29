from pymata4 import pymata4
import time

# Initialize the Pymata4 board
board = pymata4.Pymata4()

# Set digital pins 4 through 11 as outputs
for i in range(4, 12, 1):
    board.set_pin_mode_digital_output(i)

# A string containing all numerical digits for validation.
numbers_test = "0123456789"

# Pin for the seven-segment display
sevenSegmenyPin = [4, 5, 6, 7]
ser = 8  # Serial data pin
rclk = 9  # Register clock pin
srclk = 10  # Shift register clock pin

# Dictionary to map characters to their segment representation 
# Each character is represented by a list indicating whether each segment is on or off.
segment_data = {
    0: [1, 1, 1, 1, 1, 1, 0, 0],
    1: [0, 1, 1, 0, 0, 0, 0, 0],
    2: [1, 1, 0, 1, 1, 0, 1, 0],
    3: [1, 1, 1, 1, 0, 0, 1, 0],
    4: [0, 1, 1, 0, 0, 1, 1, 0],
    5: [1, 0, 1, 1, 0, 1, 1, 0],
    6: [1, 0, 1, 1, 1, 1, 1, 0],
    7: [1, 1, 1, 0, 0, 0, 0, 0],
    8: [1, 1, 1, 1, 1, 1, 1, 0],
    9: [1, 1, 1, 1, 0, 1, 1, 0],
    'blank': [0, 0, 0, 0, 0, 0, 0, 0],
    '.': [0, 0, 0, 0, 0, 0, 0, 1],
    'A': [1, 1, 1, 0, 1, 1, 1, 0],
    'B': [1, 1, 1, 1, 1, 1, 0, 0],
    'C': [1, 0, 0, 1, 1, 1, 1, 0],
    'D': [1, 1, 1, 1, 1, 0, 1, 0],
    'E': [1, 0, 0, 1, 1, 1, 1, 0],
    'F': [1, 0, 0, 0, 1, 1, 1, 0],
    'G': [1, 0, 1, 1, 1, 1, 1, 0],
    'H': [0, 1, 1, 0, 1, 1, 1, 0],
    'I': [0, 0, 1, 0, 0, 1, 0, 0],
    'J': [0, 1, 1, 1, 1, 0, 0, 0],
    'K': [1, 0, 1, 0, 1, 1, 1, 0],
    'L': [0, 0, 0, 1, 1, 1, 0, 0],
    'M': [1, 1, 1, 0, 1, 1, 0, 0],
    'N': [0, 1, 1, 0, 1, 0, 1, 0],
    'O': [1, 1, 1, 1, 1, 1, 0, 0],
    'P': [1, 1, 0, 0, 1, 1, 1, 0],
    'Q': [1, 1, 1, 0, 0, 1, 1, 0],
    'R': [0, 1, 0, 0, 1, 1, 1, 0],
    'S': [0, 0, 0, 1, 1, 0, 1, 0],
    'T': [0, 0, 0, 0, 1, 1, 1, 0],
    'U': [0, 1, 1, 1, 1, 1, 0, 0],
    'V': [0, 1, 1, 1, 1, 1, 0, 0],
    'W': [1, 1, 1, 1, 0, 1, 1, 0],
    'X': [1, 1, 1, 0, 1, 1, 1, 0],
    'Y': [1, 1, 0, 1, 1, 1, 1, 0],
    'Z': [1, 0, 1, 1, 0, 1, 1, 0]

}

# Function to display a number on a seven-segment display for a specified duration
def seven_segment(number, duration):
    number = str(number)[::-1]  # Reverse the number to process from right to left
    for a in range(4, 8, 1):
        # Ensure all seven-segment displays are off initially
        board.digital_write(a, 1)
        start_time = time.time()
    # Display the number for the duration specified
    while time.time() - start_time < duration:
        for i in range(4):  # Iterate through each digit or character
            # Determine the segment pattern for the current character
            if number[i] == ' ':
                segment = segment_data['blank']
            elif number[i] not in numbers_test:
                segment = segment_data[number[i]]
            else:
                digit = int(number[i])
                segment = segment_data[digit]
            # Reset the display before updating
            for a in range(4, 8, 1):
                board.digital_write(a, 1)
            # Update the display with the current segment pattern
            b = len(segment) - 1
            while b >= 0:
                board.digital_pin_write(ser, int(segment[b]))
                board.digital_pin_write(srclk, 1)
                board.digital_pin_write(srclk, 0)
                b -= 1
            # Latch the data onto the display
            board.digital_pin_write(rclk, 1)
            board.digital_pin_write(rclk, 0)
            # Move to the next display segment
            board.digital_write(i + 4, 0)

# Function to scroll a display text across the seven-segment displays
def scrolling_display(scroll_display):
    scroll_display = scroll_display.upper()  # Convert the display text to uppercase
    scrolling_display_list = list(scroll_display)  # Convert the text into a list of characters
    while True:
        start_time = time.time()
        display_number = ''
        for i in range(len(scrolling_display_list)):
            display_number += scrolling_display_list[i]
        # Display the current segment of the scrolling text
        if scrolling_display_list[0] != '.':
            seven_segment(display_number, 0.5 - (time.time() - start_time))
        # Rotate the display list to scroll the text
        scrolling_display_list.append(scrolling_display_list[0])
        scrolling_display_list.pop(0)

# Example usage of scrolling_display function
scrolling_display('1234 AND')
