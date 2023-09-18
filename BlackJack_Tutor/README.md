# BlackJack Strategy Tutor
- This program allows players to sharpen their BlackJack strategy by providing active assessment of their decisions as the game plays
- Players interact with a dealer at a virtual BlackJack table on a local web browser page
- Players can select specialized scenarios, like only hands with pairs, or only hands which contain an ace, allowing them to practice more difficult decisions that come up less often in real games
- Players win or lose credits and recieve an overall assessment of their decision making after quitting

## Requirements

- **Python**: 3.9
- **Package Manager**: `pip`

## Dependencies

This project relies on the following libraries:

- `Flask`
- `colorama`
- `gtts` (Google Text-to-Speech)
- `pygame`

## Installation & Setup

1. **Clone the repository**:
git clone https://github.com/AustinTD4/Projects/BlackJack_Tutor.git

2. **Navigate to the project directory**:
cd BlackJack_Tutor

3. **Set up the necessary folders**:
Create a folder named 'static' within the project directory. Move the 'images' folder into the 'static' folder.

4. **Create a virtual environment**:
python3 -m venv env
source env/bin/activate # On Windows use env\Scripts\activate

5. **Install the required libraries**:
pip install Flask colorama gtts pygame

## Usage

To use the program:

1. Open `BlackJack_Flask_Main.py`
2. Optionally, to play with a different number of decks (default is 2), provide an integer to the `startup()` method like this:
```python
startup(3)  # This will use 3 decks
```
3. Run the program
4. Once the cell runs, a link to open the virtual BlackJack table will appear in the cell output, click on this link to begin
```python
 * Running on http://127.0.0.1:1438
```
5. When playing, use `Regular', `Soft Totals', and `Pair' buttons to change the type of hands you can draw.
5. Note to not press a button before the last one has resolved, or asynchronous functions can cause errors
