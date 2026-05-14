function getComputerChoice() {
	const randomNum = Math.floor(Math.random() * 3);
	if (randomNum === 0) {
		return "rock";
	}
	if (randomNum === 1) {
		return "paper";
	}
	return "scissors";
}

function getHumanChoice() {
	let choice = Number(prompt("Choose a number between 0 and 2: "));
	if (choice === 0) {
		return "rock";
	}
	if (choice === 1) {
		return "paper";
	}
	return "scissors";
}

function playRound(humanChoice, computerChoice) {
	switch (humanChoice) {
		case "rock":
			if (computerChoice === "paper") {
				console.log(`You win! ${humanChoice} beats ${computerChoice}`);
				return "human";
				break;
			}
			if (computerChoice === "scissors") {
				console.log(`You lose! ${computerChoice} beats ${humanChoice}`);
				return "computer";
				break;
			} else {
				console.log(`You tie!`);
				return null;
				break;
			}
		case "paper":
			if (computerChoice === "rock") {
				console.log(`You win! ${humanChoice} beats ${computerChoice}`);
				return "human";
				break;
			}
			if (computerChoice === "scissors") {
				console.log(`You lose! ${computerChoice} beats ${humanChoice}`);
				return "computer";
				break;
			} else {
				console.log(`You tie!`);
				return null;
				break;
			}
		case "scissors":
			if (computerChoice === "paper") {
				console.log(`You win! ${humanChoice} beats ${computerChoice}`);
				return "human";
				break;
			}
			if (computerChoice === "rock") {
				console.log(`You lose! ${computerChoice} beats ${humanChoice}`);
				return "computer";
				break;
			} else {
				console.log(`You tie!`);
				return null;
				break;
			}
	}
}

function playGame() {
	let humanScore = 0;
	let computerScore = 0;

	for (let round = 1; round < 6; round++) {
		console.log(`Round ${round}.`);
		const humanSelection = getHumanChoice();
		const computerSelection = getComputerChoice();
		const result = playRound(humanSelection, computerSelection);
		if (result === "human") {
			humanScore++;
		} else if (result === "computer") {
			computerScore++;
		}

		console.log(`Human: ${humanScore}; Computer: ${computerScore}`);
	}

	if (humanScore > computerScore) {
		console.log(
			`You win! You had ${humanScore} points, and the computer had ${computerScore} points`,
		);
	}
	if (humanScore < computerScore) {
		console.log(
			`You lose! You had ${humanScore} points, and the computer had ${computerScore} points`,
		);
	}
	if (humanScore === computerScore) {
		console.log(
			`You tied! You had ${humanScore} points, and the computer had ${computerScore} points`,
		);
	}
}

playGame();
