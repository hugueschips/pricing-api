# pricing

This code holds a dynamic pricing API.

## Description

It has several features, such as:

- Sign-up/sign-in powered by Firebase

The main strength of pricing is it's easyness to be maintained.
To insure it stays like this:

- Speak with Daniel about your new feature
- Design independant services
- Prune useless services

## Getting Started

### Dependencies

- Python code
- Powered by poetry

### Installing locally

- Install Python 3.12 on your computer
  - on MacOS using Homebrew is recommended:
    `brew install python@3.12`
- Install make
  - on MacOS using Homebrew is recommended:
    `brew install make`
- Clone the repository
- Run the terminal command
  ` make prepare-dev``
You can now spot where your poetry env is located by running
     `poetry env info -p```

### Executing program

#### Execute locally within VS Code debugger

- Open VS Code for the repo
- Run the debug settings from .vscode/launch.json called `pricing:8000`
- You can now call the endpoint as you are used to,
  or use are Postman account where everything is necely set-up already

#### Execute without debugger

- Run the terminal command `make run`

## Help

Ask Daniel

## Authors

- Daniel Durrenberger
  - lhommelepluscl@ssedumon.de

## Expected workflow

### Git merge strategies

When developping a new feature or fix, please use the following pattern:

- checkout main branch and pull
- create a new branch using relevant prefix: feature/, bugfix/, ... and in lowercase
- commit your changes
- merge back in main using squash commit strategy.
  Please invest some effort into writing a decent merge commit message
- delete your branch remotely and locally

## Version History

- 0.0.1
  - Initial release working locally

## License

Void

## Acknowledgments
