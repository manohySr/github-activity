# GitHub Activity CLI

A command-line tool to track and analyze GitHub activity. This project is based on the [GitHub User Activity project](https://roadmap.sh/projects/github-user-activity) from roadmap.sh.

![image](https://github.com/user-attachments/assets/2347d199-c181-4ea7-94de-5b933a9a45cc)


## Features

- Fetch recent GitHub activity for any user
- Beautiful terminal output with color-coded events
- Detailed event information including:
  - Push events with commit counts
  - Repository creation
  - Branch and tag creation
  - Issues and pull requests
  - Forks and watches
  - Releases
- Graceful error handling

## Installation

### Quick Install (For Users)
```bash
pip install git+https://github.com/manohySr/github-activity.git
```


### From Source

1. Clone the repository:
```bash
git clone https://github.com/manohySr/github-activity.git
cd github-activity
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

### Project Structure

```bash
https://gitingest.com/manohySr/github-activity/
```

## Usage

Get activity for a specific GitHub user:

```bash
github-activity user <username>
```

Example output:
```
username's recent GitHub Activity:

  - Pushed 3 commits to owner/repo
  - Created a new repository: owner/repo
  - Opened issue #123: 'Issue title' in owner/repo
  - Created branch feature-branch in owner/repo
  - Starred owner/repo
```

## Development

This project uses:
- Typer for CLI interface
- Rich for beautiful terminal output
- GitHub REST API for data fetching

## License

MIT License 
