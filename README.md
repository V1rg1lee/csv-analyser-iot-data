# CSV analyser IOT data

## Prelude
This tool was originally designed for the **Embedded System Security course (ELEC-H550)**, given at the *Université Libre de Bruxelles*.

It was designed by a group comprising Martin Devolder, Virgile Devolder and Corentin Bouffioux.

## Prerequisites

### Python
To use this tool, you need Python installed on your system. Ensure you have Python version 3.7 or later. You can download the latest version of Python from the [official Python website](https://www.python.org/downloads/).

## Dataset

The dataset used for this project is available at [SmartSense on GitHub](https://github.com/snudatalab/SmartSense).

## How to Use the Dataset:
1. Download the dataset from the repository.
2. Unzip the data folder in the root directory of this project.
3. It should now have in the root directory the 4 new folders: sp, us, fr and kr.

The tool will automatically recognize and process the dataset files from the data folder.

## Launch the tool with script

### On Windows

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the following command to launch the tool:
```bash
./deploy-windows.ps1
```

### On macOS/Linux

1. Open a terminal.
2. Navigate to the project directory.
3. Run the following command to launch the tool:
```bash
chmod +x deploy-linux-macos.sh
sed -i 's/\r$//' deploy-linux-macos.sh
./deploy-linux-macos.sh
```

## Launch the tool manually

### Setting up the Environment

#### Step 1: Create a Virtual Environment
Creating a virtual environment is recommended to manage dependencies effectively and avoid conflicts.

##### On Windows:
1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the following command to create a virtual environment:
`python -m venv venv`
4. Activate the virtual environment:
`venv\Scripts\activate`

##### On macOS/Linux:
1. Open a terminal.
2. Navigate to the project directory.
3. Run the following command to create a virtual environment:
`python3 -m venv venv`
4. Activate the virtual environment:
`source venv/bin/activate`

#### Step 2: Install Required Libraries
Once the virtual environment is activated, install the required dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```
This command ensures all the necessary libraries, such as Pandas and Matplotlib, are installed.

#### Running the Scripts
Each Python script can be executed using the following command:

```bash
python <file_name>.py
```
Replace <file_name> with the actual name of the script you want to run.

## Results

The tool generates various plots and statistics based on the dataset. The results are displayed in the terminal and saved as images in the `result` folder.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
