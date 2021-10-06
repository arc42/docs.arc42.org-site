---
layout: post
title: "Example Building Block View Level-2: Traffic Pursuit Unit"
tags: buildingblock example 
category: building-block
permalink: /examples/buildingblock-2/
---


<div class="arc42-example">
This diagram (created with Enterprise Architect(TM) as a component model) shows the refinement of the measuring box including the level 2 black box descriptions. 
</div>

## 5.2 Measuring Unit (Building Block View Level 2)
The following figure shows the internal structure of the Measuring Unit. 

![Building Block View Level 2 of Traffic Pursuit Unit]({{ site.imageurl}}/examples/tpu/52-tpu-BuildingBlocks.jpg)

### 1.1 MuServices

contains the services offered by the MeasuringUnit and offers these via an RPC interface. These services are:

* deliver periodic updates of environmental and measuring data 
* perform a pursuit
* perform an automatic calibration
* perform a manual calibration
* print pursuit protocol
* print calibration data

### 1.2 Pursuit

implements the operational logic, all calculations and storage of the data of a pursuit

### 1.3 Calibrate

implements all functions to perform an automatic calibration and to permanently check the validity of the current calibration data

### 1.4 PrintService

handles layouting formatting of documents describing pursuits or calibrations and renders these according to the type of the connected printers. Implements a print queue to print thedocuments out to the attached printer.

### 1.5 SimpleTPU

implements the user interface and control logic to run a TPU without video functionality based only on the hardware and software of the Measuring Unit.

### 1.6 Config

contains all configuration data concerning the behaviour and the legal parameters for the measurements.

### 1.7 MuInit

runs only once to initialize and start up all services within the MeasuringUnit.

