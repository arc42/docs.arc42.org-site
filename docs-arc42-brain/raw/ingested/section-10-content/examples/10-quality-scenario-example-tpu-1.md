---
layout: post
title: "Example Quality Scenarios: TrafficPursuitUnit"
tags: quality example 
category: quality
permalink: /examples/quality-tpu-1/
---

<p></p>


## 10. Quality Requirements

### 10.1 Quality Tree

*Note: The (1), (2), (3) in the following table repeat the top level quality requirements from chapter 1.2.*


|Quality Category |Quality  |Description |Scenario|
| :--- | :--- | :--- | :--- |
|Usability  	|Ease of Use  (3)	|Ease of use by the policeman, especially in the use case of pursuing another car	||
| |Ease of Learning	|The standard functions should be as easy and intuitive to use as possible without the need for lengthy prior instruction |SC1|
|Performance	|Accuracy (1)	|Measurements and calculations shall be correct and precise within the specified deviation range | |
| |Comprehensiveness	|The algorithms used must be as legally watertight as possible and comprehensible	| |
| |Precision & Accuracy	 |If possible, the video insertions should be made with the granularity of a video frame	| |
| |Robustness (2)	|The system shall work reliable under all specified environment and operating conditions.| |
|Operational & Environmental	|Temperature Range |The temperature range in which the correct functioning of the device is ensured should range from -25 degrees to +85 degrees|	SC3|
|Maintainability & Support	|Maintenance & Repair |It should be possible to replace components outside the measurement box without affecting the correct measurement inside the measurement box | |
|Security |Integrity	|Verifiability of the authenticity of the video files shall be ensured with a verification code | |
|Cultural and Regional	|Multilanguage	|the texts of the user interface should be able to be converted by a translation file into different languages with ASCII character set	|SC4 |
| |Local Time Adaptability	|The time difference to Greenwich must be adjustable with a granularity of 1 minute |	|
| |Local Legal Rules Adaptability	 |the measurement procedure shall be adaptable to regional legislation	 | |
|Legal	|Legal Compliance	|Correct implementation and application of all legal requirements in the evaluation for the different types of pursuits |SC2 |

### 10.2 Quality Scenarios


|Id |Scenario |
| :--- | :--- |
|SC1 |A user who does not know the system can operate it after 10 minutes of instruction|
|SC2 |When playing a video frame by frame afterwards, each frame contains exactly the expected information|
|SC3 |Even under maximum and minimum temperature (e.g. in a climatic chamber), the device always outputs the same speed at constant pulse frequency.|
|SC4 |With appropriate translation files replacing the default language (English), all displayed and printed texts now appear in this language. |

