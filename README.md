# TEAM HTB - Last Minute Smoke Detection

We live in a difficult era. Climate change, irrelevant only a few years ago, is now the biggest challenge humanity has yet to beat. Intense droughts, storms, rising sea levels, ... are just some of the events that are becoming more and more common nowadays. Extreme temperatures, severe lightning, strong winds, dry weather and droughts create the ideal conditions for the main theme of this competition: Wildfires. 

Wildfires are one of the most frequent and recurrent disasters our world faces yearly. They burn thousands of kilometres of land a year, causing millions of dollars in damages and destroying not only the habitats of millions of species that populate our planet, but creating lasting long term effects in an already fragile planet. According to the Copernicus Atmosphere Monitoring Service scientists, global wildfires in 2021 caused an estimated total of 1760 megatonnes of carbon emissions, which is the equivalent of 6450 megatonnes of CO2. To put this figure into some perspective – total CO2 emissions from fossil fuel in the EU in 2020 amounted to 2600 megatonnes, in other words - wildfires this year generated 148% more than total EU fossil fuel emissions in 2020.

In a context where most Wildfires are created by humans, being able to detect them and respond in time is key to minimize the potential damage they will cause. 

We sadly found out about this challenge just one week ago, so we have treated it as a hackathon, prioritizing efficiency whilst trying to tackle a small subset of the problem.

# Our Project

While satellite and aerial monitoring (through the use of planes, helicopters or UAVs) can provide a wide view and may be sufficient to monitor very large, low risk terrain areas, 
we find that it is not ideal for high risk areas. The slow refresh rate of satellites and the high costs of maintaining an aerial monitoring infrastructure to track these hazard-prone areas make it highly inefficient and in most cases not feasible at all. This areas are usually monitored by means of fire lookouts.

Currently, there are some fire lookouts in towers that are used as a means of early detection of forest fires. However, accurate human observation may be limited by operator fatigue, time of day, time of year, and geographic location. Electronic systems have gained popularity in recent years as a possible resolution to human operator error. A government report on a recent trial of three automated camera fire detection systems in Australia did, however, conclude "...detection by the camera systems was slower and less reliable than by a trained human observer".

Our approach intends to breach this by using a lightweight AI-based prediction model to automatically detect the emergence of smoke. This model could be used with a real time image system to rapidly alert the authorities would it detect smoke in a given camera or recording device.

# Technical Documentation

