# Exploratory data analysis of soundscapes

The large amount of data collected during an acoustic monitoring requires a standardized workflow to store the information in a structured way, facilitate the exchange of work between researchers and speed up the data analysis. A semi-automatic workflow is proposed in order to take advantage of computer computation speed and human abstraction capacity. The first phases of the workflow are detailed in this document: (1) structuring of metadata from the audio files, (2) sub-sampling of the data for exploratory analysis, (3) visualization of the data, and (4) quantification of differences between soundscapes.


## 1. Acoustic sampling overview

When collecting data in an acoustic sampling, sensors include in each file information that is critical for further analysis. In order to automate the retrieval of this data, a script was programmed in R language that goes through all the files in a directory, extracts the metadata and structures them into a comma-separated file, or csv. The files must be nested in a directory with the name of the location and a subdirectory with the name of the sampling point. **All files must be nested in a directory with the name of the location and a subdirectory with the name of the site.**. The script [audio_metadata_utilities.R](audio_metadata_utilities.R) has all the functionswhile the script [read_audio_metadata.R](read_audio_metadata.R) is an example that show how to use the functions to get the metadata and plot a figure.

-	File name: fname_audio
-	Sample rate: sample.rate
-	Number of channels: channels
-	Number of bits: bits 
-	Number of samples: samples
-	File size: fsize
-	Recorder type: recorder_model
-	Sensor name: sensor_name
-	Formated date as "%Y-%m-%d %H:%M:%S": date
-	time: time
-	Audio file length: length
-	Name of subdirectory: site

Script names: [audio_metadata_utilities.R](audio_metadata_utilities.R), [read_audio_metadata.R](read_audio_metadata.R)

## 2. Data sub-sampling

In each acoustic monitoring, large amounts of data are recovered, in the order of Terabytes. Due to limited computing capacities and data access speed, testing and analysis of the entire data set is not efficient. A sub-sampling of this data allows to have a global vision of the data in a fast way. The script goes through a set of audio files, taking five seconds (5 s) of each file and if necessary, resamples the audio to obtain homogeneous files. The output is a pkl format file that can be easily read in Python.

Name of the script: sample_acoustic_monitoring.py

## 3.Data visualization

From the sub-sampling of the data it is extremely easy and fast to perform multiple analyses, such as calculating acoustic characteristics and visualizing data. Working with Terabyte volumes, data visualization is effective both for presenting information on large amounts of data and for directing more complex analyses. The human mind is highly trained to recognize visual patterns, and by presenting information in a raw but organized format, it is able to easily identify major trends in the data. 

A 2D representation of the sound and the 24-hour natural pulses of the soundscape was taken into account for the visualization of the acoustic monitoring data. Thus, it is proposed to calculate the spectrogram of each audio file and to organize these spectrograms in 24-hour cycles.

Script name: audio_to_spectro_image.py

## 4. Characterization of soundscapes

Data visualization allows us to quickly explore the sound recordings and even to qualitatively compare the collection sites. However, these representations are of very high dimensions and it is necessary to think about a reduction of the information. For this purpose we implemented a protocol to quantitatively characterize the acoustic characteristics of each site:

Script name: compute_psd_metrics_spectrogram.py

## 5. Quantitative analysis of soundscapes

The patterns identified by the visualization tools must be measured in order to compare the information between the sampling points and to perform a quantitative analysis. To this end, a simple and easily interpreted index was designed. The index calculates the percentage of acoustic activity by relating, from a threshold selected by the user, the number of pixels in a spectrogram that are above the threshold, divided by the pixels that are below. With this simple index it is possible to compare acoustic activity between different sites.

Script name: compute_soundscape_metrics.py
