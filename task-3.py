def hanoi(n: int, source: str = 'A', destination: str = 'C', auxiliary: str = 'B', 
          state: dict[str, list[int]] | None = None) -> dict[str, list[int]]:
    """
    Solves the Tower of Hanoi problem recursively.
    
    Args:
        n (int): Number of disks to move
        source (str): Source rod name
        destination (str): Destination rod name  
        auxiliary (str): Auxiliary rod name
        state (dict): Current state of the rods
    """
    if state is None:
        # Initialize the starting state with all disks on source rod
        state = {
            'A': list(range(n, 0, -1)),  # [n, n-1, ..., 2, 1]
            'B': [],
            'C': []
        }
        print(f"Initial state: {state}")
    
    if n == 1:
        # Base case: move one disk from source to destination
        disk = state[source].pop()
        state[destination].append(disk)
        print(f"Move disk from {source} to {destination}: {disk}")
        print(f"Intermediate state: {state}")
    else:
        # Step 1: Move n-1 disks from source to auxiliary rod
        hanoi(n-1, source, auxiliary, destination, state)
        
        # Step 2: Move the largest disk from source to destination
        disk = state[source].pop()
        state[destination].append(disk)
        print(f"Move disk from {source} to {destination}: {disk}")
        print(f"Intermediate state: {state}")
        
        # Step 3: Move n-1 disks from auxiliary to destination rod
        hanoi(n-1, auxiliary, destination, source, state)
    
    return state


def main():
    """Main function to run the Tower of Hanoi solution."""
    try:
        # Get number of disks from user input
        n = int(input("Enter the number of disks: "))
        
        if n <= 0:
            print("The number of disks must be a positive integer.")
            return
        
        # Solve the Tower of Hanoi problem
        final_state = hanoi(n)
        
        # Print final state
        print(f"Final state: {final_state}")

    except ValueError:
        print("Please enter a valid number.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")


if __name__ == "__main__":
    main()
