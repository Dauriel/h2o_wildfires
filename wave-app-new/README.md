# TEAM HTB - Last Minute Smoke Detection

We live in a difficult era. Climate change is now the biggest challenge humanity has yet to beat. Intense droughts, storms, rising sea levels, ... are just some of the events that are becoming more and more common nowadays. Extreme temperatures, severe lightning, strong winds, dry weather and droughts create the ideal conditions for the main theme of this competition: Wildfires. 

Wildfires are one of the most frequent and recurrent disasters our world faces yearly. They burn thousands of kilometres of land a year, causing millions of dollars in damages and destroying not only the habitats of millions of species that populate our planet, but creating lasting long term effects in an already fragile planet. According to the Copernicus Atmosphere Monitoring Service scientists, global wildfires in 2021 caused an estimated total of 1760 megatonnes of carbon emissions, which is the equivalent of 6450 megatonnes of CO2. To put this figure into some perspective – total CO2 emissions from fossil fuel in the EU in 2020 amounted to 2600 megatonnes, in other words - wildfires this year generated 148% more than total EU fossil fuel emissions in 2020.

Being able to detect wildfires fast and effectively, to be able to respond in time, is key to minimize the potential damage they will cause. 

### Our Project

While satellite and aerial monitoring (through the use of planes, helicopters or UAVs) can provide a wide view and may be sufficient to monitor very large, low risk terrain areas, 
we find that it is not ideal for high risk areas. These areas can be monitored by means of fire lookouts.

Currently, there are some fire lookouts in towers that are used as a means of early detection of forest fires. However, accurate human observation may be limited by operator fatigue, time of day, time of year, and geographic location. Automatic computerized systems have gained popularity in recent years as a possible resolution to human operator error. A government report on a recent trial of three automated camera fire detection systems in Australia did, however, conclude "...detection by the camera systems was slower and less reliable than by a trained human observer".

Our approach intends to solve and automate this by using a lightweight AI-based prediction model to automatically detect the emergence of smoke. This model could be used with a real time image system to rapidly alert the authorities would it detect smoke in a given camera or recording device.

Unfortunately, we found out about this challenge just one week ago, so we have treated it as a hackathon, prioritizing efficiency whilst trying to tackle a small subset of the problem.

### Technical Documentation

Our approach consists on a lightweight YoloV5s model trained to detect smoke. This model is trained over the [Wildfire Smoke Detection Dataset](https://github.com/aiformankind/wildfire-smoke-detection-research) created by [AI for Mankind](https://aiformankind.org/).

The solution is in the form of a jupyter notebook that contains detailed descriptions of each step. We developed the code on a Google Colab instance, so just by uploading it and running it fully you should obtain equivalent results to ours.

### AI WAVE App

Following the feedbacks from the first submission we developed this we application exploiting the H2O-WAVE framework. The main sections are:

* Home: this page, contains task description and technical details, along with a table reporting past predictions
* Image: allows to detect smoke given an image
* Real Time: allows to detect smoke in a video and creates data that fills the following table

![image](https://www.munichre.com/content/dam/munichre/global/images/royalty-free/GettyImages-145057928.jpg/_jcr_content/renditions/cropped.3_to_1.jpg./cropped.3_to_1.jpg =500x500)
