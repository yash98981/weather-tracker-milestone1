\# Weather Tracker - Milestone 1: HTTP Request + Server Response



\## Overview

This milestone demonstrates the fundamental concepts of making HTTP requests to external APIs and handling server responses.

\## What This Milestone Accomplishes



\### Technical Implementation

The code demonstrates:



&nbsp;\*\*Geocoding API Request\*\*

&nbsp;  - Endpoint: `https://geocoding-api.open-meteo.com/v1/search`

&nbsp;  - Converts city name to latitude/longitude coordinates

&nbsp;  - Handles location not found errors



&nbsp;\*\*Weather API Request\*\*  

&nbsp;  - Endpoint: `https://api.open-meteo.com/v1/forecast?current\_weather=true`

&nbsp;  - Retrieves current temperature, wind speed, and timestamp

&nbsp;  - Uses coordinates from geocoding step



&nbsp;\*\*Response Processing\*\*

&nbsp;  - Parses JSON responses

&nbsp;  - Extracts relevant weather data

&nbsp;  - Formats data for database storage (future milestones)





