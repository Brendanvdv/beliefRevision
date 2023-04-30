from belief_base import *

B = BeliefBase()
B = BeliefBase()
B.add(Belief('a', 4))
B.add(Belief('b', 2))
B.add(Belief('a>>b', 5))


def menu_handler():
    menu = ["See belief base", "Clean belief base",
            "Contract belief base", "Expand belief base", "Revise belief base", "Exit"]

    def display_menu():
        print("="*20)
        for i, item in enumerate(menu):
            print(f'{i + 1}. {item}')
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            choice = -1

        print("="*20)

        return choice

    while True:
        choice = display_menu()
        if choice == 1:
            if len(B.beliefs) == 0:
                print("Belief base is empty")
            for belief, order in B.orders.items():
                print(belief + ":" + str(order))
        elif choice == 2:
            if len(B.beliefs) == 0:
                print("Belief base is empty")
            else:
                B.clean()
        elif choice == 3:
            belief = input(
                "Enter belief and order in the form: belief: ")

            if len(B.beliefs) == 0:
                print("Belief base is empty")
            else:
                B.contract(belief)

        elif choice == 4:
            belief, order = input(
                "Enter belief and order in the form: belief, order: ").split()
            B.expand(Belief(belief, int(order)))
        elif choice == 5:
            belief, order = input(
                "Enter belief and order in the form: belief, order: ").split()
            B.revise(Belief(belief, int(order)))
        elif choice == 6:
            break
        else:
            print("Invalid choice")


menu_handler()
