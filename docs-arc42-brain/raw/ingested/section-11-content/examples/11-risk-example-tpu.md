---
layout: post
title: "Example Risk: TrafficPursuitUnit"
tags: risks example 
category: risks
permalink: /examples/risk-tpu-1/
---

<p></p>


## 11. Risks and Technical Debts


**Hardware  Risks**

Since we did not have any extended experience with most of the hardware components used in our system, there remained some uncertainties regarding the behavior of these components in the automotive environment, especially with regard to the temperature range, torsion and vibrations.
In contrast to the hardware components developed by our company, in the case of complex components supplied to us (e.g. CPU board), we would not be able to determine the causes of problems on our own and take remedial action. Instead, we were depend on reliable cooperation with the suppliers or manufacturers of the components. For this reason, we could not offer a comprehensive warranty, as the risk involved could not be calculated.

**Robustness of harddisks under harsh conditions**

Since at the time of the development of the system solid state disks were not avilable in the sizes needed to record big amounts of HD-video (about 1TB) and were also quite expensive, the system had to be based on harddisk. Certainly, there were special reinforced harddisks suitable for automotive conditions, but we were not able to test them in advance over several tenthousands of kilometers under the rough riding conditions that may occur in a police car. And in video recording during a pursuit, accompanied by hard manoevers of accelleration and braking, the harddisks could suffer extreme strain and torsion while writing videoclips at very high data rates.

**Software Risks**

The complexity of the third-party software used, such as the Linux operating system and the hardware drivers supplied, some of which are only available in binary code, impose a risk, that malfunctions in these parts could involve much effort in determining the cause and create a dependency from assistance of external suppliers.

