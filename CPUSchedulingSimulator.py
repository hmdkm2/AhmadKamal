import time


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
def fcfs_scheduling():
    # Ask user for the number of the processes
    Proc = int(input("Enter the number of processes: "))

    # now we will get the burst times from the user
    burst_times = []
    for i in range(Proc):
        bt = int(input(f"Enter burst time for process {i + 1}: "))
        burst_times.append(bt)

    # Initialize times
    waiting_times = [0] * Proc
    turnaround_times = [0] * Proc
    start_times = [0] * Proc
    finish_times = [0] * Proc

    # First process starts at 0
    start_times[0] = 0
    finish_times[0] = burst_times[0]
    turnaround_times[0] = burst_times[0]

    # Calculate times for other processes
    for i in range(1, Proc):
        start_times[i] = finish_times[i - 1]
        finish_times[i] = start_times[i] + burst_times[i]
        waiting_times[i] = start_times[i]
        turnaround_times[i] = burst_times[i] + waiting_times[i]

    # Print results
    print("\nProcess\tBurst Time\tStart Time\tFinish Time\tWaiting Time\tTurnaround Time")
    for i in range(Proc):
        print(
            f"P{i + 1}\t{burst_times[i]}\t\t{start_times[i]}\t\t{finish_times[i]}\t\t{waiting_times[i]}\t\t{turnaround_times[i]}")

    # Calculate average waiting and turnaround times
    avg_wt = sum(waiting_times) / Proc
    avg_tat = sum(turnaround_times) / Proc

    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    Menu()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
def sjf_non_preemptive():
    # Input and validate number of processes
    while True:
        try:
            num = int(input("Enter number of processes: "))
            if num > 0:
                break
            else:
                print("Number of processes must be positive.")
        except ValueError:
            print("Invalid input. Please enter a valid positive number.")

    processes = []  # List to store each process as [PID, Arrival Time, Burst Time]

    # Input and validate burst and arrival times for each process
    for i in range(num):
        print(f"\nProcess {i + 1}:")

        # Validate burst time (must be > 0)
        while True:
            try:
                burst = int(input("Enter burst time: "))
                if burst > 0:
                    break
                else:
                    print("Burst time must be positive.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # Validate arrival time (must be >= 0)
        while True:
            try:
                arrival = int(input("Enter arrival time: "))
                if arrival >= 0:
                    break
                else:
                    print("Arrival time must be zero or positive.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # Append process info to list
        processes.append([i + 1, arrival, burst])

    # Sort processes by Arrival Time using Bubble Sort
    for i in range(len(processes)):
        for j in range(len(processes) - 1):
            if processes[j][1] > processes[j + 1][1]:
                processes[j], processes[j + 1] = processes[j + 1], processes[j]

    current_time = 0  # Time tracker
    completed = []  # List of completed processes and their metrics
    waiting_times = []
    turnaround_times = []
    response_times = []

    # Main scheduling loop (SJF Non-preemptive)
    while processes:
        # Select processes that have arrived by current time
        ready = [p for p in processes if p[1] <= current_time]

        # If no process is ready, advance time
        if not ready:
            current_time += 1
            continue

        # Assume the first ready process has the shortest burst time
        next_proc = ready[0]

        # Loop through all ready processes
        for proc in ready:
            # If we find a process with a shorter burst time, update next_proc
            if proc[2] < next_proc[2]:
                next_proc = proc

        processes.remove(next_proc)  # Remove it from the queue

        pid, at, bt = next_proc
        start = current_time
        finish = start + bt
        wt = start - at  # Waiting time
        tat = finish - at  # Turnaround time
        rt = start - at  # Response time (same as waiting in non-preemptive)

        # Save metrics
        waiting_times.append(wt)
        turnaround_times.append(tat)
        response_times.append(rt)

        completed.append([pid, at, bt, start, finish, wt, tat, rt])
        current_time = finish  # Move current time forward

    # Display results
    print("\nPID\tAT\tBT\tStart\tFinish\tWT\tTAT\tRT")
    for p in completed:
        print(f"{p[0]}\t{p[1]}\t{p[2]}\t{p[3]}\t{p[4]}\t{p[5]}\t{p[6]}\t{p[7]}")

    # Calculate and print averages
    avg_wt = sum(waiting_times) / num
    avg_tat = sum(turnaround_times) / num
    avg_rt = sum(response_times) / num
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    print(f"Average Response Time: {avg_rt:.2f}")
    Menu()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
def preemptive_sjf():
    # Get positive integer from user input
    def get_positive_int(prompt):
        while True:
            try:
                value = int(input(prompt))
                if value <= 0:
                    print("Please enter a number greater than 0.")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    # --- INPUT SECTION ---
    # Get the number of processes
    n = get_positive_int("Enter the total number of processes: ")

    #  Get arrival times for all processes at once (space-separated)
    while True:
        try:
            arrival_times = list(map(int, input(f"Enter arrival times (space-separated) for {n} processes: ").split()))
            if len(arrival_times) != n or any(t < 0 for t in arrival_times):
                raise ValueError
            break
        except ValueError:
            print(f"Please enter exactly {n} non-negative integers.")

    # Get burst times for all processes at once (space-separated)
    while True:
        try:
            burst_times = list(map(int, input(f"Enter burst times (space-separated) for {n} processes: ").split()))
            if len(burst_times) != n or any(t < 0 for t in burst_times):
                raise ValueError
            break
        except ValueError:
            print(f"Please enter exactly {n} non-negative integers.")

    # --- INITIALIZATION SECTION ---
    arrival_burst = [[i + 1, arrival_times[i], burst_times[i]] for i in range(n)]  # Process ID, arrival, burst
    arrival_burst.sort(key=lambda x: x[1])  # Sort by arrival time

    remaining_times = burst_times[:]  # Copy of burst times
    waiting_times = [0] * n  # Initialize waiting times
    turnaround_times = [0] * n  # Initialize turnaround times
    finish_times = [0] * n  # To store completion times
    response_times = [-1] * n  # Initialize response times
    is_completed = [False] * n  # Track completed processes
    completed = 0  # Number of completed processes
    time = 0  # Current simulation time
    execution_log = []  # List of (process name, start time, end time)
    prev_index = -1  # Track previous executing process
    exec_start_time = 0  # Track the start time of a continuous run

    # --- Preemptive SCHEDULING LOOP ---
    while completed < n:
        index = -1
        min_burst = float('inf')

        # Find the shortest job available at the current time
        for i in range(n):
            if arrival_burst[i][1] <= time and not is_completed[i] and remaining_times[i] > 0:
                if remaining_times[i] < min_burst:
                    min_burst = remaining_times[i]
                    index = i
                elif remaining_times[i] == min_burst and arrival_burst[i][1] < arrival_burst[index][1]:
                    index = i

        # If a valid process is found
        if index != -1:
            if response_times[index] == -1:
                response_times[index] = time - arrival_burst[index][1]

            # Track change in process for logging
            if prev_index != index:
                if prev_index != -1:
                    execution_log.append(("P" + str(arrival_burst[prev_index][0]), exec_start_time, time))
                exec_start_time = time
                prev_index = index

            # Execute current process for 1 unit
            remaining_times[index] -= 1

            # If process completes
            if remaining_times[index] == 0:
                is_completed[index] = True
                completed += 1
                finish_times[index] = time + 1
                waiting_times[index] = finish_times[index] - arrival_burst[index][1] - burst_times[index]
                if waiting_times[index] < 0:
                    waiting_times[index] = 0

            time += 1
        else:
            # No process ready: time advances
            if prev_index != -1:
                execution_log.append(("P" + str(arrival_burst[prev_index][0]), exec_start_time, time))
                prev_index = -1
            time += 1

    # Final process execution slice
    if prev_index != -1:
        execution_log.append(("P" + str(arrival_burst[prev_index][0]), exec_start_time, time))

    # --- CALCULATE METRICS ---
    for i in range(n):
        turnaround_times[i] = burst_times[i] + waiting_times[i]

    # --- OUTPUT SECTION ---
    print("\n--- Results ---")
    print(
        "{:<8}{:<8}{:<8}{:<10}{:<12}{:<10}".format("Process", "Arrival", "Burst", "Waiting", "Turnaround", "Response"))
    for i in range(n):
        pid, arrival, burst = arrival_burst[i]
        print("{:<8}{:<8}{:<8}{:<10}{:<12}{:<10}".format(
            "P" + str(pid),
            arrival,
            burst,
            waiting_times[i],
            turnaround_times[i],
            response_times[i]
        ))

    # --- AVERAGES ---
    avg_waiting = sum(waiting_times) / n
    avg_turnaround = sum(turnaround_times) / n
    avg_response = sum(response_times) / n

    print(f"\nAverage Waiting Time   : {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Response Time  : {avg_response:.2f}")

    # --- EXECUTION TIMELINE (GANTT INFO) ---
    print("\nExecution Log (Process, Start Time, End Time):")
    print("{:<8}{:<12}{:<10}".format("Process", "Start Time", "End Time"))
    for entry in execution_log:
        print("{:<8}{:<12}{:<10}".format(entry[0], entry[1], entry[2]))
    Menu()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
def priority_scheduling():
    # Ask user for number of processes
    while True:
        try:
            Proc = int(input("Enter the number of processes: "))  # input the number of processes
            if Proc <= 0:
                print("Number of processes must be greater than 0. Try again.")  # واضحة
            else:
                break  # if it's valid, break the loop
        except ValueError:
            print(
                "Invalid input. Please enter a valid integer.")  # any input except the integer will be invalid like ("abc", "12.5", etc.)

    # To store input: (original_index, process_name, burst_time, priority)
    input_processes = []
    used_priorities = set()  # no duplicate priorities are allowed like (1, 2, 3, 4, 5) and not (1, 2, 3, 4, 4)

    for i in range(Proc):
        pname = f"P{i + 1}"  # 'f' is used to make {i + 1} active, and without it it will be like this: P{i + 1} and it will not be active

        # Get burst time
        while True:
            try:
                bt = int(input(
                    f"Enter burst time for {pname}: "))  # input the burst time for each process(this is inside a loop)
                if bt <= 0:
                    print("Burst time must be a non-negative integer and NOT Zero. Try again.")  # واضح
                else:
                    break  # if it's valid, break the loop
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        # Get and validate priority
        while True:
            try:
                pr = int(input(
                    f"Enter unique priority (1 to {Proc}) for {pname}: "))  # input the priority for each process(this is inside a loop)
                if pr < 1 or pr > Proc:
                    print(
                        f"Priority must be between 1 and {Proc}. Try again.")  # if the priority is not in the range of 1 to the number of processes, it will be invalid
                elif pr in used_priorities:  # check if the priority is already used(i explained this above)
                    print(f"Priority {pr} is already used. Enter a unique priority.")
                else:
                    used_priorities.add(pr)  # add the priority to the set of used priorities, if it's valid
                    break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        input_processes.append((i, pname, bt,
                                pr))  # add the process details to the list, and return to the loop to get the next process details

    # now we are out of loop with all the processes details, and we will sort them by their priority
    # Sort by priority (for scheduling)
    scheduled = sorted(input_processes, key=lambda x: x[
        3])  # take the 4th element of each tuple, which is the priority, then sort them in ascending order

    # Compute waiting and turnaround times based on scheduled order
    waiting_times = [0] * Proc  # assumme proc is 3 and it will be like this => waiting_times = [0, 0, 0]
    turnaround_times = [0] * Proc  # same as above, but for turnaround times

    for i in range(Proc):
        index, pname, bt, pr = scheduled[i]  # EACH process will be like this => (0, 'P1', 5, 2) and so on
        if i == 0:  # if it's the first process, there is no waiting time(basically)
            waiting = 0
        else:
            waiting = waiting_times[scheduled[i - 1][0]] + scheduled[i - 1][
                2]  # waiting time of the previous process + burst time of the previous process => P2 = P1(waiting Time) + P1(burst time)
        turnaround = bt + waiting  # Easier
        waiting_times[index] = waiting  # To understand
        turnaround_times[index] = turnaround  # with example

    # Output results in original input order
    print("\nProcess\tBurst Time\tPriority\tWaiting Time\tTurnaround Time")
    for i in range(Proc):
        _, pname, bt, pr = input_processes[i]
        print(f"{pname}\t{bt}\t\t{pr}\t\t{waiting_times[i]}\t\t{turnaround_times[i]}")

    print("\nProcess\tStart Time\tFinish Time")
    for i in range(Proc):
        print(f"P{1 + i}\t{waiting_times[i]}\t\t{turnaround_times[i]}")
    # Averages
    avg_wt = sum(waiting_times) / Proc
    avg_tat = sum(turnaround_times) / Proc

    print(f"\nAverage Waiting Time: {avg_wt:.2f}")  # .2f mean it will turn 152.3942 to 152.39
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    Menu()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
def round_robin():
    # Helper function to safely get a non-negative integer from the user
    def get_positive_int(prompt):
        while True:
            try:
                value = int(input(prompt))
                if value < 0:
                    print("Please enter a non-negative integer.")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter an integer.")

    # --- INPUT SECTION ---
    # Get the number of processes
    n = get_positive_int("Enter number of processes: ")

    # Input arrival times for all processes at once (space-separated)
    while True:
        try:
            arrival_times = list(map(int, input("Enter arrival times (space-separated): ").split()))
            if len(arrival_times) != n or any(t < 0 for t in arrival_times):
                raise ValueError
            break
        except ValueError:
            print(f"Please enter exactly {n} non-negative integers.")

    # Input burst times for all processes at once (space-separated)
    while True:
        try:
            burst_times = list(map(int, input("Enter burst times (space-separated): ").split()))
            if len(burst_times) != n or any(t < 0 for t in burst_times):
                raise ValueError
            break
        except ValueError:
            print(f"Please enter exactly {n} non-negative integers.")

    # Input the time quantum for Round Robin
    time_quantum = get_positive_int("Enter time quantum: ")

    # --- INITIALIZATION SECTION ---
    processes = [f"P{i + 1}" for i in range(n)]  # Generate process names P1, P2, ...
    remaining_times = burst_times[:]  # Copy of burst times for processing
    waiting_times = [0] * n  # Initialize waiting times to zero
    turnaround_times = [0] * n  # Initialize turnaround times
    response_times = [-1] * n  # -1 means not yet responded
    time = 0  # Current simulation time
    completed = 0  # Number of processes completed
    queue = []  # Ready queue to store process indices
    visited = [False] * n  # Tracks whether a process is in the queue
    execution_log = []  # List of (process name, start time, end time)
    context_switches = 0  # Number of context switches

    # --- ROUND ROBIN SCHEDULING LOOP ---
    while completed < n:
        # Add newly arrived processes to the ready queue
        for i in range(n):
            if arrival_times[i] <= time and not visited[i]:
                queue.append(i)
                visited[i] = True

        # If no processes are ready, increment time
        if not queue:
            time += 1
            continue

        # Pick the next process from the front of the queue
        current = queue.pop(0)

        # Record response time the first time the process gets CPU
        if response_times[current] == -1:
            response_times[current] = time

        # Calculate how much time this process will run now
        exec_time = min(time_quantum, remaining_times[current])
        start_time = time
        time += exec_time
        end_time = time
        remaining_times[current] -= exec_time

        # Log the execution slice for later display
        execution_log.append((processes[current], start_time, end_time))

        # Check if any new process has arrived while current process was executing
        for i in range(n):
            if arrival_times[i] <= time and not visited[i]:
                queue.append(i)
                visited[i] = True

        # If process is not finished, re-add it to the end of the queue
        if remaining_times[current] > 0:
            queue.append(current)
            context_switches += 1  # Context switch due to time quantum
        else:
            completed += 1
            # Calculate turnaround and waiting times
            turnaround_times[current] = time - arrival_times[current]
            waiting_times[current] = turnaround_times[current] - burst_times[current]
            if queue:
                context_switches += 1  # Context switch if next process is waiting

    # --- OUTPUT SECTION ---
    print("\n--- Results ---")
    print(
        "{:<8}{:<8}{:<8}{:<10}{:<12}{:<10}".format("Process", "Arrival", "Burst", "Waiting", "Turnaround", "Response"))
    for i in range(n):
        print("{:<8}{:<8}{:<8}{:<10}{:<12}{:<10}".format(
            processes[i],
            arrival_times[i],
            burst_times[i],
            waiting_times[i],
            turnaround_times[i],
            response_times[i]
        ))

    # --- AVERAGE CALCULATIONS ---
    avg_waiting = sum(waiting_times) / n
    avg_turnaround = sum(turnaround_times) / n
    avg_response = sum(response_times) / n

    # --- FINAL METRICS ---
    print(f"\nAverage Waiting Time   : {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Response Time  : {avg_response:.2f}")
    print(f"Total Context Switches : {context_switches}")

    # --- EXECUTION TIMELINE (GANTT INFO) ---
    print("\nExecution Log (Process, Start Time, End Time):")
    print("{:<8}{:<12}{:<10}".format("Process", "Start Time", "End Time"))
    for entry in execution_log:
        print("{:<8}{:<12}{:<10}".format(entry[0], entry[1], entry[2]))
    Menu()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to exit the program
def Exit():
    print("Exiting the program", end="")  # end = "" means it will not go to the next line after printing this
    for i in range(3):
        print(".", end="", flush=True)  # flush=True makes sure the output is printed immediately
        time.sleep(1)
    exit(0)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
def Menu():
    while True:
        print("--------------MENU--------------")
        print("please select the scheduling algorithm")
        print("1. FCFS")
        print("2. Non-Preemptive SJF")
        print("3. Preemptive SJF")
        print("4. Priority Scheduling")
        print("5. Round Robin")
        print("6. Exit")
        try:
            choice = int(input("Enter your choice: "))
            if choice < 1 or choice > 6:
                print("Invalid choice. Please select a valid option.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    if choice == 1:
        fcfs_scheduling()
    elif choice == 2:
        sjf_non_preemptive()
    elif choice == 3:
        preemptive_sjf()
    elif choice == 4:
        priority_scheduling()
    elif choice == 5:
        round_robin()
    elif choice == 6:
        Exit()
    else:
        print("Invalid choice. Please select a valid option.")


Menu()
# End of the code