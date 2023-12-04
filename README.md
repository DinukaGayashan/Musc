# Musc - music from nowhere

**Music generation using Deep Learning**

Software solution that generates musical melodies according to user preferences and requirements using Deep Learning.


## Overview

Music is called a universal language because music communicates feelings and emotions in forms of rhythm, melody, harmony, and timbre. Music composition is done by humans with their creativity, and these composers own their music. Composing of music is not an easy procedure. It requires a deep understanding, knowledge, and artistic sense.

**Musc** is using a deep learning approach to tackle this problem. With that, a desired music can be generated according to the preferences and requirements of the user.


## Features

- **Melody Generation:** Choose model, customize duration, tempo, temperature and save generated melodies.
- **Model Generation:** Upload custom datasets, generate from scratch or finetune models, and manage models.
- **View History:** View timestamped melodies, playback, save, and delete from history.


## Setup

Follow these steps to set up and run **Musc** on your local machine:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/DinukaGayashan/Musc.git
    cd musc
    ```

2. **Add Pre-trained models:**
    (Optional) Download and place pre-trained models at `models/trained_models`. Available here [here](https://www.dropbox.com/scl/fo/712kwocq97k8wnll6fkfb/h?rlkey=l54ptzdhzuuqezdd7jcmt9rwf&dl=0).

3. **Install Python:**
    Make sure Python 3.10 is installed. Download it from [python.org](https://www.python.org/).

4. **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Application:**
    ```bash
    streamlit run main.py
    ```

Or else to run with Docker by replacing steps 3 to 5:

3. **Install Docker:**
    Make sure Docker is installed. Download it from [docker.com](https://www.docker.com/).

4. **Build Docker Image:**
    ```bash
    docker build -t musc .
    ```

5. **Run with Docker:**
    ```bash
    docker run -p 8501:8501 musc
    ```

<br>

This project is highly inspired by [Pop Music Transformer: Beat-based Modeling and Generation of Expressive Pop Piano Compositions](https://paperswithcode.com/paper/pop-music-transformer-generating-music-with)

<br>

<i>Feel the magic of music with Musc!</i>
