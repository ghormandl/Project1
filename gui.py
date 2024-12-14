from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QInputDialog
from logic import VotingSystem

class VotingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voting System")
        self.setGeometry(100, 100, 400, 300)
        self.logic = VotingSystem()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        vote_layout = QHBoxLayout()
        title_label = QLabel("Enter Candidate Names (No Numbers Allowed, No Duplicates):")
        main_layout.addWidget(title_label)

        self.candidate_inputs = [QLineEdit() for _ in range(5)]
        for i, input_field in enumerate(self.candidate_inputs):
            input_field.setPlaceholderText(f"Candidate {i + 1}")
            input_layout.addWidget(input_field)

        main_layout.addLayout(input_layout)
        submit_button = QPushButton("Submit Candidates")
        submit_button.clicked.connect(self.submit_candidates)
        main_layout.addWidget(submit_button)

        self.vote_combo = QComboBox()
        self.vote_combo.setPlaceholderText("Select Candidate to Vote")
        self.vote_combo.setDisabled(True)
        self.vote_button = QPushButton("Vote")
        self.vote_button.clicked.connect(self.vote)
        self.vote_button.setDisabled(True)
        self.end_vote_button = QPushButton("End Vote")
        self.end_vote_button.clicked.connect(self.end_vote)
        self.end_vote_button.setDisabled(True)
        vote_layout.addWidget(self.vote_combo)
        vote_layout.addWidget(self.vote_button)
        vote_layout.addWidget(self.end_vote_button)
        main_layout.addLayout(vote_layout)
        self.result_label = QLabel("Votes will be displayed here.")
        main_layout.addWidget(self.result_label)
        self.setLayout(main_layout)

    def submit_candidates(self):
        """Submit candidates entered by the user."""
        candidate_names = [input_field.text().strip() for input_field in self.candidate_inputs]
        candidate_names = [name for name in candidate_names if name]

        if len(candidate_names) < 2:
            self.result_label.setText("You need at least 2 candidates to proceed.")
            return

        result = self.logic.submit_candidates(candidate_names)

        if "Error" in result or "submitted" not in result:
            self.result_label.setText(result)
            return
        for input_field in self.candidate_inputs:
            input_field.setDisabled(True)

        self.vote_combo.clear()
        self.vote_combo.addItems(self.logic.candidates)
        self.vote_combo.setEnabled(True)
        self.vote_button.setEnabled(True)
        self.end_vote_button.setEnabled(True)
        self.result_label.setText("Candidates submitted. You can now vote.")

    def vote(self):
        """Handle voting for a selected candidate."""
        voter_name, ok = QInputDialog.getText(self, "Voter Name", "Enter your name:")
        if not ok or not voter_name:
            self.result_label.setText("Voter name is required.")
            return

        selected_candidate = self.vote_combo.currentText()
        result = self.logic.vote(voter_name, selected_candidate)
        self.result_label.setText(result)
        self.show_results()

    def show_results(self):
        """Display current vote counts."""
        results = self.logic.get_results()
        self.result_label.setText(f"Current Votes:\n{results}")

    def end_vote(self):
        """End the vote, disable further voting, and shows final results."""
        self.logic.end_voting()
        self.vote_combo.setDisabled(True)
        self.vote_button.setDisabled(True)
        self.end_vote_button.setDisabled(True)
        final_results = self.logic.get_results()
        self.result_label.setText(f"Voting Ended. Final Results:\n{final_results}")