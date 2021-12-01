---
layout: post
title: "Example Concept: TrafficPursuitUnit Domain Entity Model"
tags: concept example 
category: concept
permalink: /examples/concept-tpu-1/
---

## 8. Crosscutting Concepts

### 8.1 Domain Entity Model

![Fig. 8.1: Domain Entity Model]({{ site.imageurl}}/examples/tpu/III81_DomainEntityModel.jpg)


| Term | Definition |
| :--- | :--- |
|Frame Interval	|the smallest period for data sampled by the TPU. It corresponds to the duration of one video frame, which is 40 milliseconds for a frequency of 25 videoframes per second |
|Distance Per Frame	|the distance (in millimeters) travelled during one frame|
|Distance Per Second	|the distance (in millimeters) travelled during one second |
|Pursuit Step	 |the measured and calculated data for one second within a pursuit. It consists of  pursuit duration, distance, current speed, current maximum violation.| 
|Pursuit Step File	|a file containing all pursuit steps |
|Pursuit File	|a file containing the video, the pursuit step file and the printout for one pursuit.|
|Pursuit Protocol	|second-by-second logging of the driven speed + pursuit summary |
|Sector	|a part of a complete pursuit | 
|Video Frame |one picture within a video stream. Usually we have 25 frames per second. | 

