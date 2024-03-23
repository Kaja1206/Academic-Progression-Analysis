# I declare that my work contains no examples of misconduct, such as plagiarism, or collusion

# Any code taken from other sources is referenced within my code solution

#student ID : 20221080
#date :10/11/2023

from graphics import GraphWin, Point, Line, Text, Rectangle, GraphicsError

progression_outcomeList = []  # array to store the progression outcomes


def get_progression_outcome_count(outcomes):
    outcome_count = {}
    for outcome in outcomes:
        progression_outcome = outcome[0]
        outcome_count[progression_outcome] = outcome_count.get(progression_outcome, 0) + 1
    return outcome_count


def main():
    # printing the menu
    while True:
        try:
            print("\n---------------------menu-----------------------")
            print("1. Calculate the Progression Outcome of Students")
            print("2. Display the data")
            print("3. Save the data to a file")
            print("4. Retrieve data from the saved file")
            print("5. Exit\n")

            # determining the option from the user
            option = int(input("Enter the preferred option: "))

            # IF loop to determine and call the function for the required option chosen
            if option == 1:
                calculate_outcome()

            elif option == 2:
                print("\nPart2:")
                for outcome in progression_outcomeList:
                    print(f"{outcome[0]} - {outcome[1]}, {outcome[2]}, {outcome[3]}")
                display_histogram_results(get_progression_outcome_count(progression_outcomeList))
                main()

            elif option == 3:
                save_data(progression_outcomeList)

            elif option == 4:
                retrieved_data = retrieve_data()
                if retrieved_data is not None:
                    progression_outcomeList.extend(retrieved_data)
                main()

            elif option == 5:
                quit()

            else:
                print("Enter a valid option and try again!!")

        except ValueError:
            print("Invalid input data type. Enter a valid integer option! ")

#function to calculate outcome
def calculate_outcome():
    while True:
        pass_credits = valid_input("\nPlease enter the number of pass credits: ", [0, 20, 40, 60, 80, 100, 120])
        defer_credits = valid_input("Please enter the number of defer credits: ", [0, 20, 40, 60, 80, 100, 120])
        fail_credits = valid_input("Please enter the number of fail credits: ", [0, 20, 40, 60, 80, 100, 120])

        outcome = progression_outcome(pass_credits, defer_credits, fail_credits)
        print(outcome)

        if outcome not in ["Out of Range", "Total incorrect"]:
            progression_outcomeList.append([outcome, pass_credits, defer_credits, fail_credits])

        while True:
            continue_using = input(
                "\nWould you like to enter another set of data? \nEnter 'y' for yes or 'q' to quit and view results: ")
            if continue_using.lower() in ['q', 'y']:
                break
            else:
                print("Invalid input. Please enter either 'q' to quit or 'y' to continue.\n")

        if continue_using.lower() == 'q':
            break
        elif continue_using.lower() != 'y':
            print("Invalid input. Please enter either 'q' to quit or 'y' to continue.\n")

#function to determine the outcome
def progression_outcome(pass_creds, defer_creds, fail_creds):
    total_creds = pass_creds + defer_creds + fail_creds

    if (pass_creds not in range(0, 140, 20)) or (defer_creds not in range(0, 140, 20)) or (fail_creds not in
                                                                                           range(0, 140, 20)):
        return "Out of Range"
    elif total_creds != 120:
        return "Total incorrect"
    elif pass_creds == 120:
        return "Progress"
    elif pass_creds == 100:
        return "Progress (module trailer)"
    elif pass_creds in [60, 80]:
        return "Module retriever"
    elif pass_creds == 40 and fail_creds != 80:
        return "Module retriever"
    elif pass_creds == 20 and fail_creds not in [80, 100]:
        return "Module retriever"
    elif pass_creds == 0 and fail_creds not in [80, 100, 120]:
        return "Module retriever"
    elif total_creds == 120:
        return "Exclude"


def valid_input(prompt, valid_values):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_values:
                return value
            else:
                print("Out of range\n")
        except ValueError:
            print("Integer required\n")


# function to save the inputs
def save_data(data):
    try:
        with open('data', 'w') as file:
            for outcome in data:
                file.write(f"{outcome[0]} - {outcome[1]}, {outcome[2]}, {outcome[3]}\n")

        print("Data has been save to " + 'data')
        main()
    except IOError as error:
        print("Error: " + error)


# function to retrieve the inputs
def retrieve_data():
    try:
        with open('data', 'r') as file:
            data = []

            for line in file:
                parts = line.strip().split(' - ')

                if len(parts) == 2:
                    outcome, credits_info = parts
                    credits = list(map(int, credits_info.split(', ')))

                    if len(credits) == 3:
                        pass_credits, defer_credits, fail_credits = credits
                        data.append((outcome, pass_credits, defer_credits, fail_credits))

        print("Data retrieval is successfully completed")
        return data

    except IOError as error:
        print("Error: " + str(error))
        return None


def display_histogram_results(progression_outcome_count):
    # Display histogram results
    win = GraphWin("Histogram Results", 440, 350)
    win.setBackground("white")

    # x-axis
    x_axis = Line(Point(10, 251), Point(430, 251))
    x_axis.draw(win)

    # Header
    header = Text(Point(100, 30), f"Histogram Results")
    header.draw(win)

    # Colors for different outcomes
    colors = {"Progress": "green",
              "Progress (module trailer)": "yellow",
              "Do not Progress – module retriever": "red",
              "Exclude": "gray"}

    bar_width = 80
    bar_height = 50
    x_axis = 30
    y_axis = 250

    # Initialize the total progression outcome count
    total_progression_outcome_count = 0

    for progression_outcome, count in progression_outcome_count.items():
        # Display progression outcome
        display_progression_outcome = progression_outcome.replace("Progress (module trailer)", "Trailer").replace(
            "Do not Progress – module retriever", "Retriever")

        bar_color = colors.get(progression_outcome, "blue")
        bar = Rectangle(Point(x_axis, y_axis), Point(x_axis + bar_width, y_axis - bar_height * count))
        bar.setFill(bar_color)
        bar.draw(win)

        outcomes = Text(Point(x_axis + bar_width / 2, y_axis + 30), f"{display_progression_outcome}: {count}")
        outcomes.draw(win)

        x_axis += bar_width + 30

        # Total progression outcome count
        total_progression_outcome_count += count

    # Display the total outcomes
    total_outcomes = Text(Point(100, 300), f"{total_progression_outcome_count} outcomes in total. ")
    total_outcomes.draw(win)

    try:
        win.getMouse()
        win.close()
    except GraphicsError as GE:
        print(f"An error occurred: {GE}")


main()

#---------references-----------
#https://www.w3schools.com/python/default.asp
#https://www.javatpoint.com/python-tutorial
