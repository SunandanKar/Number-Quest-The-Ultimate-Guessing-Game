import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QProgressBar, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QEvent

class InstructionsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Instructions')
        self.setGeometry(450, 250, 450, 250)
        self.setStyleSheet("background-color: #F0F8FF;")  # Alice blue background

        layout = QVBoxLayout()

        instruction_label = QLabel("Welcome to the Number Guessing Game! 🎉\n\n"
                                   "1. The game will generate a random number between 1 and 100.\n"
                                   "2. Your goal is to guess the number within 10 attempts.\n"
                                   "3. After each guess, you will receive feedback on how close you are.\n"
                                   "4. If you guess the number or use up all attempts, the game will end.\n\n"
                                   "Click 'Start Game' to begin!", self)
        instruction_label.setFont(QFont("Arial", 14))
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("color: #000000;")  # Black color
        layout.addWidget(instruction_label)

        start_button = QPushButton("Start Game", self)
        start_button.setFont(QFont("Arial", 14, QFont.Bold))
        start_button.setStyleSheet("background-color: #32CD32; color: white; padding: 10px;")  # Lime green
        start_button.clicked.connect(self.accept)
        layout.addWidget(start_button)

        self.setLayout(layout)

class GuessingGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the window
        self.setWindowTitle('Colorful Number Guessing Game')
        self.setGeometry(200, 100, 900, 600)  # Larger window size
        self.setStyleSheet("background-color: #F5F5DC;")  # Beige background

        # Create main layout
        self.main_layout = QVBoxLayout()

        # Title label with custom font and color
        self.title_label = QLabel("🎉 Guess the Number! 🎉", self)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setStyleSheet("color: #8A2BE2;")  # Blue-violet color
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # Instruction label
        self.instruction_label = QLabel("Guess a number between 1 and 100:", self)
        self.instruction_label.setFont(QFont("Arial", 16))
        self.instruction_label.setStyleSheet("color: #2E8B57;")  # Sea green color
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.instruction_label)

        # Input field for guesses
        self.input = QLineEdit(self)
        self.input.setFont(QFont("Arial", 16))
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setStyleSheet("border: 2px solid #4682B4; padding: 10px; background-color: #FAFAD2;")  # Light goldenrod yellow background
        self.main_layout.addWidget(self.input)

        # Submit button with custom color and font
        self.submit_button = QPushButton("Submit Guess", self)
        self.submit_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.submit_button.setStyleSheet("background-color: #FF1493; color: white; padding: 12px;")  # Deep pink
        self.submit_button.clicked.connect(self.check_guess)
        self.main_layout.addWidget(self.submit_button)

        # Progress bar to show remaining attempts
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFont(QFont("Arial", 14))
        self.progress_bar.setStyleSheet("QProgressBar { border: 2px solid #B0C4DE; border-radius: 5px; }"
                                        "QProgressBar::chunk { background-color: #00CED1; }")  # Dark turquoise
        self.main_layout.addWidget(self.progress_bar)

        # Feedback label (status message) placed above the table
        self.feedback_label = QLabel("", self)
        self.feedback_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.feedback_label)

        # Table layout
        self.table_layout = QVBoxLayout()
        
        # Table to show guessed numbers and their statuses
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Guess", "Status"])
        self.table.setFont(QFont("Arial", 14))
        self.table.setStyleSheet("QTableWidget { border: 2px solid #B0C4DE; border-radius: 5px; background-color: #FAFAD2; }"
                                 "QHeaderView::section { background-color: #FFE4B5; }")  # Moccasin color
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 400)

        # Set table to be read-only
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table_layout.addWidget(self.table)
        
        self.main_layout.addLayout(self.table_layout)

        # Restart button
        self.restart_button = QPushButton("Restart Game", self)
        self.restart_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.restart_button.setStyleSheet("background-color: #FFD700; color: black; padding: 12px;")  # Gold
        self.restart_button.clicked.connect(self.restart_game)
        self.restart_button.setEnabled(False)
        self.main_layout.addWidget(self.restart_button)

        # Status label below the progress bar
        self.status_label = QLabel("", self)
        self.status_label.setFont(QFont("Arial", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.status_label)

        # Set the layout to the window
        self.setLayout(self.main_layout)

        # Initialize game variables
        self.max_attempts = 10
        self.random_number = None
        self.attempts = 0
        self.game_started = False

        # Install event filter to handle key presses
        self.installEventFilter(self)

        # Show instructions dialog
        self.show_instructions()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.handle_enter_key()
                return True
        return super().eventFilter(obj, event)

    def handle_enter_key(self):
        if not self.game_started:
            self.start_game()
        else:
            self.check_guess()

    def show_instructions(self):
        dialog = InstructionsDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.start_game()

    def start_game(self):
        print("Starting a new game...")  # Debugging print statement
        self.random_number = random.randint(1, 100)
        self.attempts = 0
        self.progress_bar.setMaximum(self.max_attempts)
        self.progress_bar.setValue(self.max_attempts)
        self.status_label.setText(f"Attempts Left: {self.max_attempts}")  # Update status label
        self.feedback_label.setText("")
        self.submit_button.setEnabled(True)
        self.input.setEnabled(True)
        self.input.clear()
        self.restart_button.setEnabled(True)  # Enable the restart button
        self.submit_button.show()  # Ensure the button is visible
        self.game_started = True
        self.submit_button.setText("Submit Guess")
        self.table.setRowCount(0)  # Clear previous guesses

    def check_guess(self):
        if not self.game_started:
            QMessageBox.warning(self, "Game Not Started", "Please start the game by clicking 'Start Game'.")
            return

        try:
            guess = int(self.input.text())
            
            if guess < 1 or guess > 100:
                QMessageBox.warning(self, "Invalid Guess", "Please enter a number between 1 and 100.")
                return

            self.attempts += 1
            remaining_attempts = self.max_attempts - self.attempts

            # Update progress bar
            self.progress_bar.setValue(remaining_attempts)
            self.status_label.setText(f"Attempts Left: {remaining_attempts}")  # Update status label

            # Check the user's guess with new proximity feedback
            if guess < self.random_number - 5:
                self.feedback_label.setText("🔻 Too low! Try again.")
                self.feedback_label.setStyleSheet("color: #FF4500;")  # Orange red
            elif guess > self.random_number + 5:
                self.feedback_label.setText("🔺 Too high! Try again.")
                self.feedback_label.setStyleSheet("color: #FF6347;")  # Tomato
            elif self.random_number - 5 <= guess < self.random_number:
                self.feedback_label.setText("⬇️ You are just low! Try again.")
                self.feedback_label.setStyleSheet("color: #FFA500;")  # Orange
            elif self.random_number < guess <= self.random_number + 5:
                self.feedback_label.setText("⬆️ You are just high! Try again.")
                self.feedback_label.setStyleSheet("color: #FFA500;")  # Orange
            else:
                self.feedback_label.setText(f"🎉 Correct! You guessed it in {self.attempts} attempts.")
                self.feedback_label.setStyleSheet("color: #32CD32;")  # Lime green
                self.end_game(True)
                return

            # Add the guess and status to the table
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(guess)))
            self.table.setItem(row_position, 1, QTableWidgetItem(self.feedback_label.text()))

            # Center-align table items
            self.table.item(row_position, 0).setTextAlignment(Qt.AlignCenter)
            self.table.item(row_position, 1).setTextAlignment(Qt.AlignCenter)

            # Scroll to the bottom of the table
            self.table.scrollToBottom()

            if remaining_attempts == 0:
                self.end_game(False)

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")

    def end_game(self, won):
        print("Game ended. Won:", won)  # Debugging print statement
        if won:
            self.feedback_label.setText(f"🎉 Correct! The number was {self.random_number}.")
            self.feedback_label.setStyleSheet("color: #32CD32;")  # Lime green
        else:
            self.feedback_label.setText(f"❌ Game Over! The number was {self.random_number}.")
            self.feedback_label.setStyleSheet("color: #FF6347;")  # Tomato

        self.submit_button.setEnabled(False)
        self.submit_button.hide()  # Hide the submit button
        self.input.setEnabled(False)
        self.restart_button.setEnabled(True)

    def restart_game(self):
        print("Restarting game...")  # Debugging print statement
        self.start_game()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GuessingGame()
    game.show()
    sys.exit(app.exec_())
