#!/usr/bin/env bash

# Ensure script exits on errors
set -e

# Command-line argument or prompt for project name
if [ -n "$1" ]; then
  PROJECT_NAME="$1"
else
  echo "Enter the project name:"
  read -e PROJECT_NAME
  if [ -z "$PROJECT_NAME" ]; then
    echo "Error: Project name cannot be empty."
    exit 1
  fi
fi

PARENT_DIR="projects"
if [ ! -d "$PARENT_DIR" ]; then
  echo "Creating parent directory: $PARENT_DIR"
  mkdir -p "$PARENT_DIR"
fi

# Generate timestamped directory name
TIMESTAMP=$(date +"%m-%d-%Y-%H-%M-%S")
PROJECT_DIR="$PARENT_DIR/${PROJECT_NAME}-${TIMESTAMP}"
CODEBASE_DIR="$PROJECT_DIR/codebase"
METADATA_FILE="$PROJECT_DIR/metadata.txt"
INDEX_FILE="$PROJECT_DIR/codebase_index.faiss"
#PROMPT_FILE="$PROJECT_DIR/default_prompt.txt"
PROMPT_FILE="default_prompt.txt"

# Create project directory
mkdir -p "$CODEBASE_DIR"
cd "$PROJECT_DIR" || exit 1

# Command-line argument or prompt for repository URL or local directory
if [ -n "$2" ]; then
  INPUT_PATH="$2"
else
  echo "Enter the GitHub repository URL or path to the local directory containing the codebase:"
  read -e INPUT_PATH
fi

# Clone or copy the codebase
if [[ "$INPUT_PATH" =~ ^http ]]; then
  # Clone Git repository
  echo "Cloning repository into $CODEBASE_DIR..."
  cd codebase
  git clone "$INPUT_PATH" .
  cd ..
elif [ -d "$INPUT_PATH" ]; then
  # Copy local directory
  echo "#############################"
  pwd
  echo "#############################"
  echo "Copying local directory into $CODEBASE_DIR..."
  #cp -r "$INPUT_PATH"/* "$CCODEBASE_DIR"
  cp -r "$INPUT_PATH" codebase/
else
  echo "Error: Invalid Git repository URL or local directory path."
  exit 1
fi

# Set default prompt
echo "Enter a default prompt for the system (leave blank for generic):"
read -e DEFAULT_PROMPT
if [ -z "$DEFAULT_PROMPT" ]; then
  DEFAULT_PROMPT="You are an assistant knowledgeable about the given codebase. Answer questions and provide insights."
fi
  echo "#############################"
  echo "making promp file from directory:"
  pwd
  echo "#############################"
echo "$DEFAULT_PROMPT" > "$PROMPT_FILE"

# Prepare FAISS index
echo "Codebase Directory: $CODEBASE_DIR"
echo "FAISS Index File: $INDEX_FILE"
echo "Metadata File: $METADATA_FILE"
  echo "#############################"
  echo "preparing FAISS index from directory:"
  pwd
  echo "#############################"

echo "Preparing the FAISS index..."
python ../../prepare_codebase.py "../../$CODEBASE_DIR" "../../$INDEX_FILE" "../../$METADATA_FILE"

echo "Setup complete. Project directory: $PROJECT_DIR"
echo "To start interacting, run: python ../interact_with_codebase.py $PROJECT_DIR"


##!/usr/bin/env bash

## Ensure script exits on errors
#set -e

## Validate project name
#if [ -z "$1" ]; then
#  echo "Usage: setup_project.sh <project-name> [repo-url or local-directory]"
#  exit 1
#fi

#PROJECT_NAME="$1"
#TIMESTAMP=$(date +"%m-%d-%Y-%H-%M-%S")
#PROJECT_DIR="./${PROJECT_NAME}-${TIMESTAMP}"
#CODEBASE_DIR="$PROJECT_DIR/codebase"
#METADATA_FILE="$PROJECT_DIR/metadata.txt"
#INDEX_FILE="$PROJECT_DIR/codebase_index.faiss"
#PROMPT_FILE="$PROJECT_DIR/default_prompt.txt"

## Create project directory
#mkdir -p "$CODEBASE_DIR"
#cd "$PROJECT_DIR" || exit 1

## Handle codebase input
#if [ -n "$2" ]; then
#  if [[ "$2" =~ ^http ]]; then
#    # Clone Git repository
#    git clone "$2" "$CODEBASE_DIR"
#  elif [ -d "$2" ]; then
#    # Copy local directory
#    cp -r "$2"/* "$CODEBASE_DIR"
#  else
#    echo "Error: Invalid Git repository URL or local directory path."
#    exit 1
#  fi
#else
#  echo "Enter the path to a local directory containing the codebase:"
#  read -e LOCAL_DIR
#  if [ -d "$LOCAL_DIR" ]; then
#    cp -r "$LOCAL_DIR"/* "$CODEBASE_DIR"
#  else
#    echo "Error: Invalid directory. Exiting."
#    exit 1
#  fi
#fi

## Set default prompt
#echo "Enter a default prompt for the system (leave blank for generic):"
#read -e DEFAULT_PROMPT
#if [ -z "$DEFAULT_PROMPT" ]; then
#  DEFAULT_PROMPT="You are an assistant knowledgeable about the given codebase. Answer questions and provide insights."
#fi
#echo "$DEFAULT_PROMPT" > "$PROMPT_FILE"

## Prepare FAISS index
#echo "Preparing the FAISS index..."
#python ../prepare_codebase.py "$CODEBASE_DIR" "$INDEX_FILE" "$METADATA_FILE"

#echo "Setup complete. Project directory: $PROJECT_DIR"
#echo "To start interacting, run: python ../interact_with_codebase.py $PROJECT_DIR"


###!/usr/bin/env bash

### ollama_feeder/setup_project.sh
##set -e

##echo "Enter the project name:"
##read -e PROJECT_NAME

##if [ -z "$PROJECT_NAME" ]; then
##  echo "Project name cannot be empty."
##  exit 1
##fi

##PROJECT_DIR="./projects/$PROJECT_NAME"
##CODEBASE_DIR="$PROJECT_DIR/codebase"
##METADATA_FILE="$PROJECT_DIR/metadata.txt"
##INDEX_FILE="$PROJECT_DIR/codebase_index.faiss"
##PROMPT_FILE="$PROJECT_DIR/default_prompt.txt"

### Create project directory
##mkdir -p "$PROJECT_DIR"
##mkdir -p "$CODEBASE_DIR"

### Clone a repository or ask for a directory
##echo "Enter the GitHub repository URL (or press Enter to provide a local directory):"
##read -e REPO_URL

##if [ -n "$REPO_URL" ]; then
##  git clone "$REPO_URL" "$CODEBASE_DIR"
##else
##  echo "Enter the path to the local directory containing the codebase:"
##  read -e LOCAL_DIR
##  if [ -d "$LOCAL_DIR" ]; then
##    cp -r "$LOCAL_DIR"/* "$CODEBASE_DIR"
##  else
##    echo "Invalid directory. Exiting."
##    exit 1
##  fi
##fi

### Set default prompt
##echo "Enter a default prompt for the system (leave blank for generic):"
##read -e DEFAULT_PROMPT
##if [ -z "$DEFAULT_PROMPT" ]; then
##  DEFAULT_PROMPT="You are an assistant knowledgeable about the given codebase. Answer questions and provide insights."
##fi
##echo "$DEFAULT_PROMPT" > "$PROMPT_FILE"

### Prepare FAISS index
##echo "Preparing the FAISS index..."
##python prepare_codebase.py "$CODEBASE_DIR" "$INDEX_FILE" "$METADATA_FILE"

##echo "Setup complete. To start interacting, run: python interact_with_codebase.py $PROJECT_DIR"


####!/usr/bin/env bash

#### ollama_feeder/run.sh
###set -e

#### Step 1: Clone a repository
###echo "Enter the GitHub repository URL (or press Enter to skip):"
###read -e REPO_URL
###if [ -n "$REPO_URL" ]; then
###  git clone "$REPO_URL" codebase
###fi

#### Step 2: Set default prompt
###echo "Enter a default prompt for the system (leave blank for generic):"
###read -e DEFAULT_PROMPT
###if [ -z "$DEFAULT_PROMPT" ]; then
###  DEFAULT_PROMPT="You are an assistant knowledgeable about the given codebase. Answer questions and provide insights."
###fi
###echo "$DEFAULT_PROMPT" > default_prompt.txt

#### Step 3: Prepare FAISS index
###echo "Preparing the FAISS index..."
###python prepare_codebase.py

#### Step 4: Start interactive session
###echo "Setup complete. Starting interactive session..."
###python interact_with_codebase.py

