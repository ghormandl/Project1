import csv
import os

class VotingSystem:
    def __init__(self):
        self.candidates = []
        self.votes = {candidate: 0 for candidate in self.candidates}
        self.voting_ended = False
        self.vote_file = 'votes.csv'

    def submit_candidates(self, candidate_names):
        """Submit candidates and initialize their vote counts."""
        if len(candidate_names) != len(set(candidate_names)):
            return "Duplicate candidates are not allowed."
        for name in candidate_names:
            if any(char.isdigit() for char in name):
                return "Candidate names cannot contain numbers."
        if len(candidate_names) < 2:
            return "You need at least 2 candidates to proceed."

        self.candidates = candidate_names
        self.votes = {candidate: 0 for candidate in self.candidates}
        self.voting_ended = False

        with open(self.vote_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['voter_name', 'candidate_name'])
        return "Candidates submitted successfully."

    def vote(self, voter_name, candidate_name):
        """Cast a vote for a candidate."""
        if self.voting_ended:
            return "Voting has ended. No more votes can be cast."
        if candidate_name not in self.candidates:
            return "Invalid candidate."
        has_voter, existing_name = self.has_voted(voter_name)
        if has_voter:
            return f"{existing_name}, you have already voted."

        self.votes[candidate_name] += 1
        self.save_vote(voter_name, candidate_name)
        return f"Vote casted for {candidate_name}."

    def has_voted(self, voter_name):
        """Check if a voter has already voted and return their name."""
        if not os.path.exists(self.vote_file):
            return False, ""
        with open(self.vote_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == voter_name:
                    return True, row[0]
        return False, ""

    def save_vote(self, voter_name, candidate_name):
        """Save the vote to the CSV file."""
        with open(self.vote_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([voter_name, candidate_name])

    def get_results(self):
        """Return the current vote counts."""
        if not self.candidates:
            return "No candidates to display results for."
        return "\n".join([f"{candidate}: {votes}" for candidate, votes in self.votes.items()])

    def end_voting(self):
        """End the voting process, preventing further votes."""
        self.voting_ended = True
        return "Voting has ended."