import turtle
import argparse
import sys


def koch_side(t: turtle.Turtle, length: float, n: int) -> None:
    """
    Draw one side of Koch snowflake using recursion.
    
    Args:
        t: Turtle object
        length: Length of the line segment
        n: Recursion level
    """
    if n == 0:
        t.forward(length)
    else:
        # Divide into 4 segments with specific angles
        koch_side(t, length / 3, n - 1)
        t.left(60)
        koch_side(t, length / 3, n - 1)
        t.right(120)
        koch_side(t, length / 3, n - 1)
        t.left(60)
        koch_side(t, length / 3, n - 1)


def draw_koch_snowflake(level: int) -> None:
    """
    Draw complete Koch snowflake with specified recursion level.
    
    Args:
        level: Recursion level for the fractal
    """
    # Set up the screen
    screen = turtle.Screen()
    screen.title(f"Koch Snowflake - Level {level}")
    screen.bgcolor("white")
    screen.setup(800, 600)
    
    # Show progress for high levels
    if level > 4:
        print(f"Drawing Koch snowflake with recursion level {level}...")
        print("This may take some time. Please wait...")
    
    # Create turtle
    t = turtle.Turtle()
    t.speed(0)
    t.color("blue")
    
    # Starting position and length
    length = 300
    
    # Move to starting position
    t.penup()
    t.goto(-length / 2, length / 3)
    t.pendown()
    
    # Draw three sides of the snowflake
    for _ in range(3):
        koch_side(t, length, level)
        t.right(120)
    
    # Hide turtle after drawing
    t.hideturtle()
    
    # Keep window open with multiple exit options
    print("Drawing complete! Click on the window or press any key to close.")
    print("You can also press Ctrl+C in terminal to force close.")
    
    # Set up multiple ways to close
    screen.onclick(lambda x, y: screen.bye())  # Close on click
    screen.onkey(lambda: screen.bye(), "space")  # Close on spacebar
    screen.onkey(lambda: screen.bye(), "Escape")  # Close on Escape
    screen.onkey(lambda: screen.bye(), "q")  # Close on 'q' key
    screen.listen()
    
    try:
        screen.mainloop()
    except turtle.Terminator:
        pass  # Handle window close gracefully


def get_level_from_input() -> int:
    """
    Get recursion level from user input with validation.
    
    Returns:
        int: Valid recursion level
    """
    print("Koch Snowflake Fractal Generator")
    print("=" * 35)
    
    while True:
        try:
            # Get recursion level from user
            level_input = input("Enter recursion level (0-6 recommended): ")
            level = int(level_input)
            
            # Validate input
            if level < 0:
                print("Error: Recursion level must be non-negative")
                continue
            
            if level > 6:
                print("Warning: High recursion levels may take a long time to render")
                confirm = input("Continue? (y/n): ")
                if confirm.lower() != 'y':
                    print("Cancelled.")
                    continue
            
            return level
            
        except ValueError:
            print("Error: Please enter a valid integer")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
            sys.exit(0)


def main() -> None:
    """
    Main function - supports both argparse and input methods.
    """
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        # Use argparse for command line arguments
        parser = argparse.ArgumentParser(description="Draw Koch Snowflake fractal")
        parser.add_argument(
            "level",
            type=int,
            help="Recursion level for the Koch snowflake (0-6 recommended)"
        )
        
        try:
            args = parser.parse_args()
            level = args.level
            
            # Validate input
            if level < 0:
                print("Error: Recursion level must be non-negative")
                return
            
            if level > 6:
                print("Warning: High recursion levels may take a long time to render")
            
        except SystemExit:
            # argparse calls sys.exit on error or --help
            return
            
    else:
        # No command line arguments provided, use interactive input
        level = get_level_from_input()
    
    # Draw the snowflake
    print(f"Drawing Koch snowflake with level {level}...")
    draw_koch_snowflake(level)


if __name__ == "__main__":
    main()