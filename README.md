# [“Seeing” Electric Network Frequency from Events](https://xlx-creater.github.io/E-ENF/)

### [Project Page](https://xlx-creater.github.io/E-ENF/) | [Paper](https://arxiv.org/pdf) | [Data](https://whueducn-my.sharepoint.com/:f:/g/personal/2018302120267_whu_edu_cn/En7DQ7Sg-KhIjeHlphDd1sIBA7alS2xg6UqKfbWf0E-3Zg?e=9aDKcG)

<img src='https://github.com/xlx-creater/E-ENF/blob/main/Illustration.png'/> 

> [“Seeing” Electric Network Frequency from Events](https://xlx-creater.github.io/E-ENF/) 
>
>  [Lexuan Xu](https://scholar.google.com.hk/citations?hl=zh-CN&user=g3itm8IAAAAJ), [Guang Hua](https://ghua-ac.github.io/), [Haijian Zhang](https://scholar.google.com/citations?user=cEWbejoAAAAJ&hl=zh-CN&oi=ao), [Lei Yu](https://scholar.google.com/citations?user=Klc_GHUAAAAJ&hl=zh-CN), [Ning Qiao](https://scholar.google.com/citations?user=e7FIdOMAAAAJ&hl=zh-CN&oi=ao)
>
> IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR2023)


## Prepare Data

Download the datasets from [EV-ENFD](https://whueducn-my.sharepoint.com/:f:/g/personal/2018302120267_whu_edu_cn/En7DQ7Sg-KhIjeHlphDd1sIBA7alS2xg6UqKfbWf0E-3Zg?e=9aDKcG).


1. Place one or several raw event files in the '.aedat4' format under the three scenarios in EV-ENFD into the 'Events/Raw/'.
2. Run 'Event_Process/aedat4_unpack_without_flir.py' to decompress the '.aedat4' files in 'Raw', and save the results in 'Events/Unpacked'.
3. Replace 'Events/ENF_Reference' with the 'ENF_Reference' folder in EV-ENFD, where each '.wav' file contains grid voltage changes recorded by the transformer within an hour.


Untar the downloaded archive into `data/` sub-folder in the code directory.

See NeRF++ sections on [data](https://github.com/Kai-46/nerfplusplus#data) and [COLMAP](https://github.com/Kai-46/nerfplusplus#generate-camera-parameters-intrinsics-and-poses-with-colmap-sfm) on how to create adapt a new dataset for training. 

Please contact us if you need to adapt your own event stream as it might need updates to the code.

## Create environment

```
conda env create --file environment.yml
conda activate eventnerf
```

## Training and Testing

Use the scripts from `scripts/` subfolder for training and testing.
Please replace `<absolute-path-to-code>` and `<path-to-conda-env>` in the `.sh` scripts and the corresponding `.txt` config file
To do so automatically for all of the files, you can use `sed`:
```
sed 's/<absolute-path-to-code>/\/your\/path/' configs/**/*.txt scripts/*.sh
sed 's/<path-to-conda-env>/\/your\/path/' scripts/*.sh
```

## Models

 - `configs/nerf/*`, `configs/lego1/*` -- synthetic data,
 - `configs/nextgen/*`, `configs/nextnextgen/*` -- real data (from the revised paper),
 - `configs/ablation/*` -- ablation studies,
 - `configs/altbase.txt` -- constant window length baseline,
 - `configs/angle/*` -- camera angle error robustness ablation,
 - `configs/noise/*` -- noise events robustness ablation,
 - `configs/deff/*` -- data efficiency ablation (varying amount of data by varying the simulated event threshold),
 - `configs/e2vid/*` -- synthetic data e2vid baseline,
 - `configs/real/*` -- real data (from the old version of the paper)

## Mesh Extraction

To extract the mesh from a trained model, run

```
ddp_mesh_nerf.py --config nerf/chair.txt
```

Replace `nerf/chair.txt` with the path to your trained model config.


## Evaluation
Please find the guide on evaluation, color-correction, and computing the metrics in [`metric/README.md`](https://github.com/r00tman/EventNeRF/blob/main/metric/README.md).

## Citation

Please cite our work if you use the code.

```
@InProceedings{rudnev2023eventnerf,
      title={EventNeRF: Neural Radiance Fields from a Single Colour Event Camera},
      author={Viktor Rudnev and Mohamed Elgharib and Christian Theobalt and Vladislav Golyanik},
      booktitle={Computer Vision and Pattern Recognition (CVPR)},
      year={2023}
}
```

## License

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/) or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
