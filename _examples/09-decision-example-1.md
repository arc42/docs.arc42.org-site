---
layout: post
title: "Example Decision: TrafficPursuitUnit"
tags: decition example 
category: decision
permalink: /examples/decision-tpu-1/
---

## 9. Architecture Decisions


**Efficient Calculation**
 
In order to perform calculations as quickly as possible and to save CPU power, all calculations are performed with integers (fixed point). Float calculations are only used if unavoidable (e.g. root extraction for Pythagorean theorem).

**Buffering of Video Information**

The propagation of measurement data from the MeasuringUnit via the VideoUnit to the VideoSubsystem has to pass via serial lines and may suffer variable delays during the processing within the different nodes. We decided to achieve a fixed delay, such that the data rendered on the screen exactly represents the real time behaviour shifted by a fixed time delay. This is achieved by keeping a buffer of video information to be displayed in the video inserter software.  The display of the first piece of information is delayed until the buffer has accumulated a reserve of 5 data items. This precaution assures that every video frame can be supplied with current data at the right time. The system has a constant delay of 200 milliseconds (5 Frames * 40 ms time per frame), so the exact data corresponding to video frame number n can be found in the data inserted into frame number n + 5.

**Performance tuning in the interface to the codec driver**

The software for controlling the video codec initially existed as an external separate process with a command interface. To improve the response time after commands, a functional interface was created and the control software was integrated into its own process.
