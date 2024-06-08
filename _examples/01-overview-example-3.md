---
layout: post
title: "Overview Example: Traffic Pursuit Unit"
tags: overview example 
category: overview
permalink: /examples/overview-example-3/
---

<div class="arc42-example">
<br>
After a short introductory text explaining the system under design a table of key project goals is given and an overview of the functionality is shown as use case diagram with accompaning table
</div>

## 1. Introduction 
This document describes the Traffic Pursuit Unit, short TPU, which is a speed measuring device equipped with video recording facilities that is installed within a policecar. It is used to measure and record the speed profile of a car driving in front of the policecar, so that speed limit violations can be proved and legal action can be taken based on the documentation and video recordings produced by the system.
The current development is based on an existing version of the system, that has been developed by the same companies, and shall take the product to a new release with added and improved featurers enabled by the latest developments in hardware technology.

The following goals have been established for this system:

| Priority |  |
| :--- | :--- |
|1	|The system shall be enhanced by features that are suitable to keep and strenghten the position as the current market leader |
|2 |The system shall implement HD resolution for video clips and storage of the clips to harddisk.|
|3	|All system parts that are due to legal approval shall be contained in one unit (called MeasuringUnit), so that replacement of other parts of the system will not require reapproval of the device.|
|4	|The MeasuringUnit shall be able to run autonomously and be marketed as a low cost variant of TPU without video proof.|
|5	|The operable temperature range shall be expanded to a range of at least -25 to 85 degrees Celsius.|


## 1.1 Requirements

![Introduction]({{ site.imageurl }}/examples/tpu/1-UseCases.jpg)

| Id | Requirement | Explanation |
| :--- | :--- | --- |
|F1|Perform automatic calibration|perform an automatic calibration by means of GPS information|
|F1.1|Print calibration protocol| |
|F2|Perform a pursuit of a car|follow a car driving at too high speed in order to create a proving documentation|
|F3|Show List of all recorded pursuits| |
|F4|Play recording of a pursuit |replay the video documentation of a pursuit case i.e. to show it to the car driver in charge |
|F5|Print protocol of a pursuit| | 
|F6 |Show basic information | in idle state the system shall display default information like date and time and the current speed| 





