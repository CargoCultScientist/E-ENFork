# [“Seeing” Electric Network Frequency from Events](https://xlx-creater.github.io/E-ENF/)

### [Project Page](https://xlx-creater.github.io/E-ENF/) | [Paper](https://arxiv.org/pdf/2305.02597.pdf) | [Data](https://whueducn-my.sharepoint.com/:f:/g/personal/2018302120267_whu_edu_cn/En7DQ7Sg-KhIjeHlphDd1sIBA7alS2xg6UqKfbWf0E-3Zg?e=9aDKcG)

<img src='https://github.com/xlx-creater/E-ENF/blob/main/Illustration.png'/> 

> [“Seeing” Electric Network Frequency from Events](https://xlx-creater.github.io/E-ENF/) 
>
>  [Lexuan Xu](https://scholar.google.com.hk/citations?hl=zh-CN&user=g3itm8IAAAAJ), [Guang Hua](https://ghua-ac.github.io/), [Haijian Zhang](https://scholar.google.com/citations?user=cEWbejoAAAAJ&hl=zh-CN&oi=ao), [Lei Yu](https://scholar.google.com/citations?user=Klc_GHUAAAAJ&hl=zh-CN), [Ning Qiao](https://scholar.google.com/citations?user=e7FIdOMAAAAJ&hl=zh-CN&oi=ao)
>
> IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR2023)


## Prepare Data

Download the datasets from [EV-ENFD](https://whueducn-my.sharepoint.com/:f:/g/personal/2018302120267_whu_edu_cn/En7DQ7Sg-KhIjeHlphDd1sIBA7alS2xg6UqKfbWf0E-3Zg?e=9aDKcG).


1. Place one or several raw event files in the '.aedat4' format under the three scenarios in EV-ENFD into the 'Events/Raw/'.
2. Run 'Event_Process/aedat4_unpack_without_flir.py' to unpack '.aedat4' files in 'Raw', and the result will be saved in 'Events/Unpacked/dvSave-' (containing two folders: 'events' for unpacked events and 'event2ts' for frame-compressed event stream in time surface mode).
3. Replace 'Events/ENF_Reference' with the 'ENF_Reference' folder in EV-ENFD, where each '.wav' file contains grid voltage changes recorded by the transformer within an hour.


After performing the aforementioned operations, the contents of the 'Events' folder are as follows:
```
<project root>
  |-- Events
  |     |-- Raw
  |     |     |-- dvSave-2022_08_17_20_10_23.aedat4
  |     |     |-- dvSave-2022_08_17_20_24_41.aedat4
  |     |     |-- ...
  |     |-- Unpacked
  |     |     |-- dvSave-2022_08_17_20_10_23
  |     |     |    |-- events
  |     |     |    |-- event2ts
  |     |     |-- dvSave-2022_08_17_20_24_41
  |     |     |    |-- events
  |     |     |    |-- event2ts
  |     |     |-- ...     
  |     |-- ENF_Reference
  |     |     |-- 2022_08_17_Wed_17_00_00.wav
  |     |     |-- 2022_08_17_Wed_18_00_00.wav
```


## Estimate Electric Network Frequency using E-ENF

<img src='https://github.com/xlx-creater/E-ENF/blob/main/GUI.png' />

To use the GUI interface shown above, run 'E_ENF/E_ENF(GUI)/ENF_match_GUI.py' and follow these steps:

1. Click on the 'Unpacked Events' button and select the desired event stream from the 'Events/Unpacked/dvSave-/events' folder (e.g., 'dvSave-2022_08_17_20_10_23/events') for extraction.
2. Select the real ground truth reference by clicking on the 'ENF_Reference Folder' button and choosing the 'Events/ENF_Reference' folder.
3. Press the 'Start' button to initiate the estimation of the ENF signal from the selected event stream. The estimated result will be displayed in the middle of the GUI.


## Citation

Please cite our work if you use the code.

```
@inproceedings{xu2023seeing,
  title={"Seeing" Electric Network Frequency From Events},
  author={Xu, Lexuan and Hua, Guang and Zhang, Haijian and Yu, Lei and Qiao, Ning},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={18022--18031},
  year={2023}
}
```


## Additional comments on the fork:
Thr program is focused on estimating Electric Network Frequency (ENF) fluctuations from event streams recorded by event cameras. This approach, referred to as E-ENF (Event-based ENF), is designed to overcome the limitations of conventional Video-based ENF (V-ENF) methods, especially in challenging environments. Let's synthesize how the scripts work together in the context of this study:

### Objective of the Study
- **ENF Estimation from Event Streams**: The primary aim is to estimate ENF fluctuations, which are implicit in the flickering of artificial lights, from the data captured by event cameras. Unlike traditional cameras that capture frame-based videos, event cameras record data as a stream of events based on changes in light intensity, providing high temporal resolution and dynamic range.

### Role of Each Script in the Study:
**Data Unpacking** (unpack and unpack_events_file Functions):
These functions handle the extraction of event data from .aedat4 files.
This data is crucial for the E-ENF estimation as it contains the high-resolution event information captured by the event cameras.

**Event Data Processing** (Event_txt_loader Class):
This class processes the unpacked event data, organizing it into a structured format. It is particularly useful for handling and analyzing the spatio-temporal characteristics of the events, which are key to understanding ENF fluctuations in different scenarios.

**Visualization of Event Data** (event_timesurface Function and events2timesurfaces Function):
These components are used to visualize the event data as time surface images. While this may not directly contribute to ENF estimation, it provides a valuable tool for analyzing and understanding the event data, which could be beneficial for validating and interpreting the results of the E-ENF method.
Overall Functionality in the Context of the Study
The program seems to form part of a larger system designed to implement the E-ENF estimation method. It likely fits into the initial stages of the E-ENF pipeline, where event data is extracted, processed, and potentially visualized for further analysis.
The E-ENF method itself, which would include mode filtering and harmonic enhancement to extract ENF traces from event data, may be implemented in parts of the code not provided here. The provided scripts lay the groundwork for data handling and preliminary analysis.
Application in the Study
In the context of the Event-Video ENF Dataset (EV-ENFD) mentioned in the text above, these scripts could be used to process and analyze the event data captured under various conditions (static, dynamic, extreme lighting).
This preprocessing is essential for the subsequent E-ENF analysis, where accurate ENF traces are extracted, especially in challenging conditions where V-ENF methods fall short.
In summary, the scripts you've provided play a crucial role in handling, processing, and visualizing event data from neuromorphic sensors, setting the stage for advanced E-ENF analysis in various environmental conditions. This aligns with the study's goal of developing a robust method for ENF estimation using event-based camera data.