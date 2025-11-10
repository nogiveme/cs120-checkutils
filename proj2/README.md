
# CS120-PJ2 - Test Toolkit

This project provides a suite of tools designed to test the robustness of Athernet data transmission.

It consists of two main components:
1.  **`check.py`**: A data generation and verification tool. It can generate a binary file of a standard size (6250 bytes) based on a simple numeric key (00-99) and compare two files (e.g., "INPUT.bin" vs. "OUTPUT.bin") for similarity.
2.  **`jammer.py`**: An audio jammer. It simulates environmental interference by playing intermittent white noise, allowing you to test your data transmission protocol's resilience to noise.


## 📋 Dependencies

This project requires Python 3 and the `sounddevice` and `numpy` libraries.

```bash
pip install sounddevice numpy
````

-----

## 🛠️ Component 1: `check.py` (Verification Tool)

This script is used to generate reproducible test data and verify the results of a transmission.

### Usage

`check.py` has three modes of operation:

1.  **Generate `INPUT.bin` (Random Key)**

    ```bash
    python check.py
    ```

      * **Action**: Generates a new random key (00-99) and uses it to create the `INPUT.bin` file.
      * **Output**:
        ```
        No arguments provided. Generating INPUT.bin with random key...
        using key: 42  <-- Take note of this key!
        generated: INPUT.bin (6250 bytes)
        ```
      * **Note**: `INPUT.bin` is now your "ground truth" data. **You must remember this key (e.g., `42`)** to reproduce it on the receiving end.

2.  **Generate `OUTPUT.bin` (From Known Key)**

    ```bash
    python check.py <key>
    ```

      * **Example**: `python check.py 42`
      * **Action**: Uses the key you provide (e.g., `42`) to regenerate the identical data file, saving it as `OUTPUT.bin`. This is used on the receiving end to create the "ground truth" for comparison.
      * **Note**: This script will not overwrite an existing file.

3.  **Compare Two Files**

    ```bash
    python check.py <file1> <file2>
    ```

      * **Example**: `python check.py OUTPUT.bin received_data.bin`
      * **Action**: Performs a binary comparison of the two files and reports their similarity.
      * **Output**:
        ```
        ==================================================
        file 1: OUTPUT.bin (6250 bytes)
        file 2: received_data.bin (5800 bytes)
        matches: 5800/6250
        similarity: 92.80%
        identical: no ✗
        ==================================================
        ```

-----

## 🔉 Component 2: `jammer.py` (Audio Jammer)

This script is used to create audio interference during your data transmission.

### Usage

1.  **Run the script**
    ```bash
    python jammer.py
    ```
2.  **Select Device**
      * The script will first list all available audio output devices.
      * **Example Output**:
        ```
        Available audio devices:
        Index 0: Microsoft Sound Mapper - Input - 0
        Index 1: 耳机 (iKF-King-S Hands-Free AG Au - 0
        Index 2: Line In /Microphone (Waves Soun - 0
        Index 3: 麦克风 (Realtek(R) Audio) - 0
        Index 4: 麦克风 (Steam Streaming Microphone - 0
        Index 5: Microsoft Sound Mapper - Output - 0
        Index 6: 耳机 (iKF-King-S Stereo) - 0
        Index 7: 扬声器 (Steam Streaming Speakers) - 0
        Index 8: 扬声器 (Realtek(R) Audio) - 0
        Index 9: Realtek Digital Output (Realtek - 0
        Index 10: 扬声器 (Waves SoundGrid) - 0
        Index 11: 扬声器 (Steam Streaming Microphone - 0
        Index 12: 耳机 (iKF-King-S Hands-Free AG Au - 0
        Index 13: 主声音捕获驱动程序 - 1
        Index 14: 耳机 (iKF-King-S Hands-Free AG Audio) - 1
        Index 15: Line In /Microphone (Waves SoundGrid) - 1
        Index 16: 麦克风 (Realtek(R) Audio) - 1
        Index 17: 麦克风 (Steam Streaming Microphone) - 1
        Index 18: 主声音驱动程序 - 1
        Index 19: 耳机 (iKF-King-S Stereo) - 1
        Index 20: 扬声器 (Steam Streaming Speakers) - 1
        ......
        ```
      * Enter the **index** of the output device you wish to use for playing the noise (e.g., 18 for 主声音驱动程序).
3.  **Jamming Begins**
      * The script will start looping, playing 50-100ms of white noise followed by 100-200ms of silence.
      * Press `Ctrl+C` to stop the script.

-----

## 🔬 Full Experiment Workflow (Example)

Assume you have a "sender" program and a "receiver" program (the main part of your project, not included in this toolkit).

1.  **[Sender] - Generate Source Data**

      * Run `python check.py`.
      * Assume it generates `INPUT.bin` and prints `using key: 73`.

2.  **[Jammer] - (Optional) Start Interference**

      * On another computer (or on the sender/receiver), run `python jammer.py` and select a speaker.
      * The jamming noise will begin playing.

3.  **[Sender/Receiver] - Perform Data Transmission**

      * **[Sender]**: Run your sender program, which reads `INPUT.bin` and "plays" it through its speaker.
      * **[Receiver]**: Run your receiver program, which "records" the sound from its microphone and decodes the data, saving it as `received.bin`.

4.  **[Receiver] - Verify Data**

      * You know the original key was `73`.
      * **Step 4a: Re-generate the "Ground Truth"**
          * Run `python check.py 73`.
          * This creates `OUTPUT.bin`, which is **identical** to the sender's `INPUT.bin`.
      * **Step 4b: Compare the Result**
          * Run `python check.py OUTPUT.bin received.bin`.
          * Check the `similarity` percentage to evaluate the **success rate** of your acoustic data link, either with or without interference.

