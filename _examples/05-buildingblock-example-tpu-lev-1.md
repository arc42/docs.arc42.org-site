---
layout: post
title: "Example Building Block View Level-1: Traffic Pursuit Unit"
tags: buildingblock example 
category: building-block
permalink: /examples/buildingblock-tpu-1/
---


<div class="arc42-example">
<br>
This Level 1 diagram has been created with Enterprise Architect(TM) as a component diagram. It is augmented by a list of black box descriptions for each building block. 
</div>

## 5.1 Building Block View Level 1
The following figure shows the internal top-level decomposition of the Traffic Pursuit Unit. The decomposition is mainly driven by the deployment of these top-level building blocks to different hardware (cf. chapter 7). Note that the blue boxes are pure software blocks, while the white one is still a mixture of hardware and software functionality.

![Building Block View Level 1 of Traffic Pursuit Unit]({{ site.imageurl}}/examples/tpu/51-tpu-BuildingBlocks.jpg)

### 1. Measuring Unit

is responsible for all measurements (speed, time, GPS data, temperature, pursuit data) and for the calculation and storing of all legally relevant data.
It can run standalone, without being attached to the VideoUnit, doing simple pursuits without video. In this case it implements an own simple user interface by means of a keyboard with alphanumeric display.

### 2. VideoUnit

controls the operation of the MeasuringUnit (when it is not operating standalone). It collects all current data from the MeasuringUnit, formats it and dispatches it to the UserInserter and the LegalInserter for display.

It also implements the graphical user interface and the functionality for creating, storing and managing videos.

By communicating with the PowerControl module it performs a safe shutdown when ignition is being turned off.

### 3. Video Subsystem

summarizes all hardware and software functionality running on the video boards. It handles all video operations from incoming video frames to their display on the screen including all transitions between analog and digital video signals. It contains the codec that compresses the video stream from recording and decodes recorded videoclips for playback.
 
### 4. PowerControl


is responsible for monitoring of the ignition state, in order to support a regular shutdown of the Linux System. After the shutdown the TPU can safely be powered off to prevent it from draining the battery of the car.  When the ignition being turned off, this component communicates this fact to the VideoUnit in order to request shutdown, and waits for the information, that the system is safely shut down. Then it powers off the TPU.

### Important Interfaces

**MeasuringUnit-If**

This interface provides all functionality to control and access the measuring functionality of the Measuring Unit. It is implemented by remote procedure call, and can be accessed as well internally as externally by another node.
