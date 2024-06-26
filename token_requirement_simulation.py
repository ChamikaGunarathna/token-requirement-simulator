import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Function to simulate the player potions
def getPlayerDivisions(num_players,low_score_pp_mean,high_score_pp_mean,low_score_pp_variance,high_score_pp_variance):
    
    #adjusting percentage to float
    low_score_pp_mean*=0.01
    high_score_pp_mean*=0.01
    low_score_pp_variance*=0.01
    high_score_pp_variance*=0.01
    #low score player numbers
    ls = round(num_players*random.uniform(low_score_pp_mean-low_score_pp_variance,
                                                    low_score_pp_mean+low_score_pp_variance))
    #high score player numbers
    hs = round(num_players*random.uniform(high_score_pp_mean-high_score_pp_variance,
                                                    high_score_pp_mean+high_score_pp_variance))

    #mid score player numbers
    ms = num_players - ls-hs
    
    return ls,ms,hs

# Function to simulate the scores list of the players
def calculateScoreListSingleMatch(num_players,max_score_points,low_score_pp_mean,high_score_pp_mean,low_score_pp_variance,high_score_pp_variance):
    score_list = []
    low_score_num_players,mid_score_num_players,high_score_num_players = getPlayerDivisions(num_players,low_score_pp_mean,high_score_pp_mean,low_score_pp_variance,high_score_pp_variance)
    #low scores
    for i in range(low_score_num_players):
        score = round(random.uniform(0, 0.25*max_score_points))
        score_list.append(score)
        
    #medium scores
    for i in range(mid_score_num_players):
        score = round(random.uniform(0.25*max_score_points, 0.75*max_score_points))
        score_list.append(score)

    #high scores
    for i in range(high_score_num_players):
        score = round(random.uniform(0.75*max_score_points, max_score_points))
        score_list.append(score)
    
    return score_list

# Function to calculate the scores per match
def calculateTotalScoresPerMatch(scores_matches):
    total_scores_per_match =[]
    for item in scores_matches:
        total_scores_per_match.append(np.sum(item))
    return total_scores_per_match

# Function to calculate the scores per player
def calculateTotalScoresPerPlayer(scores_matches):
    total_scores =[]
    for item in scores_matches:
        for i in item:
            total_scores.append(i)
    return total_scores

# Function to plot the histograms
def plot_histogram(data,name):
    mean = np.mean(data)
    std = np.std(data)
    
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(data, bins=10, alpha=0.7, color='blue', edgecolor='black')
    
    # Add labels and axis
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of {name}')
    
    ax.axvline(mean, color='red', linestyle='dashed', linewidth=1,label='Mean')
    ax.axvline(mean + std, color='green', linestyle='dashed', linewidth=1,label='Mean + Std')
    ax.axvline(mean - std, color='green', linestyle='dashed', linewidth=1,label='Mean - Std')

    # Adding legend
    ax.legend()
    return fig

# Function to be called when the button is clicked
def on_simulate_button_click():
    isError = False
    try:
        num_matches = int(entry_num_of_matches.get())
        min_num_players = int(entry_min_players.get())
        max_num_players = int(entry_max_players.get())
        max_score_points = float(entry_max_score_poits.get())
        low_score_pp_mean = float(entry_low_score_mean.get())
        high_score_pp_mean = float(entry_max_score_mean.get())
        low_score_pp_variance = float(entry_low_score_variance.get())
        high_score_pp_variance = float(entry_max_score_variance.get())
        xp_to_sprts = float(entry_xp_to_sprt.get())
        
        # checking the input parameters
        result=""
        if (num_matches<0) or (min_num_players<0) or (max_num_players<0) or (max_score_points<0) or (low_score_pp_mean<0) or (high_score_pp_mean<0) or (low_score_pp_variance<0) or (high_score_pp_variance<0) or (xp_to_sprts<0):
            result = result+f"\n"+"Inputs can't be negative"
            isError = True
        if max_num_players < min_num_players:
            result = result+f"\n"+"Max players should be greater than or equal to min players"
            isError = True
        if(isError):
            messagebox.showwarning("Inputs Invalid",result)
        else:
            # array for storing simulated result
            scores_matches =[]
            
            for match in range(num_matches):
                num_players = random.randint(min_num_players,max_num_players)
                scores_match = calculateScoreListSingleMatch(num_players,max_score_points,low_score_pp_mean,high_score_pp_mean,low_score_pp_variance,high_score_pp_variance)
                scores_matches.append(scores_match)
            
            # Create a button to show the results per match
            label_result_per_match = tk.Label(root, text="Results Simulted for a Single Match : ", anchor="w")
            label_result_per_match.grid(row=7, column=0, columnspan=4, pady=10)
            match_results_button = tk.Button(root, text="Show", command=lambda:on_match_results_click(scores_matches,xp_to_sprts,min_num_players,max_num_players))
            match_results_button.grid(row=7, column=1,columnspan=4, pady=10)
            
            # Create a button to show the results per player
            label_result_per_player = tk.Label(root, text="Results Simulted for a Single Player : ", anchor="w")
            label_result_per_player.grid(row=9, column=0, columnspan=4, pady=10)
            player_results_button = tk.Button(root, text="Show", command=lambda:on_player_results_click(scores_matches,xp_to_sprts,min_num_players,max_num_players))
            player_results_button.grid(row=9, column=1,columnspan=4, pady=10)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers")

# Function to be called when the "Show Results" button is clicked
def on_match_results_click(scores_match,xp_to_sprts,min_players,max_players):
    # Create a new window
    result_window = tk.Toplevel(root)
    result_window.title("Results per Match")
    result_window.geometry("800x600")
    
    data = calculateTotalScoresPerMatch(scores_match)
    fig = plot_histogram(data,"Match")
    
    # Add a canvas widget to display the Matplotlib plot
    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky=tk.NSEW)
    
    # Configure grid row and column weights to make the plot expandable
    result_window.grid_rowconfigure(0, weight=1)
    result_window.grid_columnconfigure(0, weight=1)
    
    mean = np.mean(data)
    std = np.std(data)
    
    label_total_data = tk.Label(result_window, text=f"Total Matches : {len(data)}")
    label_total_data.grid(row=1, column=0, padx=10, pady=5, sticky="n")

    result1 =f"For a match with players randomly varying between {min_players}-{max_players}\n\tScores Mean \t: {round(mean,2)}\n\tScores std \t: {round(std,2)}"
    label_result1 = tk.Label(result_window, text=result1)
    label_result1.grid(row=2, column=0, padx=10, pady=5, sticky="n")
    
    result2 =f"\nTherefore the required tokens amount per match would be;\n\tTokens Mean \t: {round(mean/xp_to_sprts,4)}\n\t Tokens std \t: {round(std/xp_to_sprts,4)}"
    label_result2 = tk.Label(result_window, text=result2)
    label_result2.grid(row=3, column=0, padx=10, pady=5, sticky="n")

# Function to be called when the "Show Results" button is clicked
def on_player_results_click(scores_match,xp_to_sprts,min_players,max_players):
    # Create a new window
    result_window = tk.Toplevel(root)
    result_window.title("Results for Player")
    result_window.geometry("800x600")
    
    data = calculateTotalScoresPerPlayer(scores_match)
    fig = plot_histogram(data,"Match")
    
    # Add a canvas widget to display the Matplotlib plot
    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky=tk.NSEW)
    
    # Configure grid row and column weights to make the plot expandable
    result_window.grid_rowconfigure(0, weight=1)
    result_window.grid_columnconfigure(0, weight=1)
    
    mean = np.mean(data)
    std = np.std(data)
    
    label_total_data = tk.Label(result_window, text=f"Total Players : {len(data)}")
    label_total_data.grid(row=1, column=0, padx=10, pady=5, sticky="n")

    result1 =f"For a match with players randomly varying between {min_players}-{max_players}\n\tScore per Player Mean \t: {round(mean,2)}\n\tScore per Player std \t: {round(std,2)}"
    label_result1 = tk.Label(result_window, text=result1)
    label_result1.grid(row=2, column=0, padx=10, pady=5, sticky="n")
    
    result2 =f"\nTherefore the required tokens amount per match would be;\n\tTokens per Player Mean \t: {round(mean/xp_to_sprts,4)}\n\tTokens per Player std \t: {round(std/xp_to_sprts,4)}"
    label_result2 = tk.Label(result_window, text=result2)
    label_result2.grid(row=3, column=0, padx=10, pady=5, sticky="n")
    
    
# Create the main window
root = tk.Tk()
root.title("Simulate Number of Tokens Required")

# Create labels and entry widgets for number inputs
label1 = tk.Label(root, text="Enter Number of Matches:")
label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_num_of_matches = tk.Entry(root)
entry_num_of_matches.grid(row=0, column=1, padx=10, pady=5)
entry_num_of_matches.insert(0, "1000")

# Create labels and entry widgets for number inputs
label2 = tk.Label(root, text="Enter Minimum Number of Players:")
label2.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_min_players = tk.Entry(root)
entry_min_players.grid(row=1, column=1, padx=10, pady=5)
entry_min_players.insert(0, "700")

# Create labels and entry widgets for number inputs
label3 = tk.Label(root, text="Enter Maximum Number of Players:")
label3.grid(row=1, column=2, padx=10, pady=5, sticky="e")
entry_max_players = tk.Entry(root)
entry_max_players.grid(row=1, column=3, padx=10, pady=5)
entry_max_players.insert(0, "1200")

# Create labels and entry widgets for number inputs
label4 = tk.Label(root, text="Enter Max Score Points a Player Can get in a Match:")
label4.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_max_score_poits = tk.Entry(root)
entry_max_score_poits.grid(row=2, column=1, padx=10, pady=5)
entry_max_score_poits.insert(0, "100")

# Create labels and entry widgets for number inputs
label5 = tk.Label(root, text="Enter Low Scoring Player Mean (%):")
label5.grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_low_score_mean = tk.Entry(root)
entry_low_score_mean.grid(row=3, column=1, padx=10, pady=5)
entry_low_score_mean.insert(0, "60")

# Create labels and entry widgets for number inputs
label7 = tk.Label(root, text="Enter Low Scoring Player Variance (%):")
label7.grid(row=3, column=2, padx=10, pady=5, sticky="e")
entry_low_score_variance = tk.Entry(root)
entry_low_score_variance.grid(row=3, column=3, padx=10, pady=5)
entry_low_score_variance.insert(0, "5")

# Create labels and entry widgets for number inputs
label6 = tk.Label(root, text="Enter High Scoring Player Mean (%):")
label6.grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_max_score_mean = tk.Entry(root)
entry_max_score_mean.grid(row=4, column=1, padx=10, pady=5)
entry_max_score_mean.insert(0, "10")

# Create labels and entry widgets for number inputs
label8 = tk.Label(root, text="Enter High Scoring Player Variance (%):")
label8.grid(row=4, column=2, padx=10, pady=5, sticky="e")
entry_max_score_variance = tk.Entry(root)
entry_max_score_variance.grid(row=4, column=3, padx=10, pady=5)
entry_max_score_variance.insert(0, "5")

# Create labels and entry widgets for number inputs
label9 = tk.Label(root, text="Enter Player Points to SPRT Conversion Ratio:")
label9.grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_xp_to_sprt = tk.Entry(root)
entry_xp_to_sprt.grid(row=5, column=1, padx=10, pady=5)
entry_xp_to_sprt.insert(0, "1000")

# Create a button widget
simulate_button = tk.Button(root, text="Simulate", command=on_simulate_button_click)
simulate_button.grid(row=6, column=0,columnspan=4, pady=10)

# Run the application
root.mainloop()