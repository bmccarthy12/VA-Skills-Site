# **Virginia VRC Skills Rankings**  

This project provides a **real-time leaderboard** for **VEX Robotics Competition (VRC) teams in Virginia**, displaying the highest skills scores based on API data from RobotEvents. The system automates data retrieval, processing, and website updates using AWS services.

---

## **🚀 Features**
✅ **Dynamic Website with React**  
- Built with **React.js** to display **ranked team skills scores**.  
- Highlights **qualified teams (green)** and **potential qualifiers (yellow)** dynamically.  

✅ **Automated Data Collection with AWS Lambda**  
- Uses a **Python AWS Lambda function** to fetch **skills scores** from the RobotEvents API.  
- Extracts **each team’s best event-based programming and driver scores**.  
- Saves processed data to **AWS S3** for static site updates.  

✅ **Scheduled Updates with AWS EventBridge**  
- Lambda runs on a **daily schedule** via **AWS EventBridge**, ensuring fresh data.  

✅ **Fast & Cost-Effective Hosting with S3 & CloudFront**  
- The React site is **deployed to an AWS S3 bucket** and served through **CloudFront**.  
- CloudFront provides **fast global access** with caching and HTTPS support.  

---

## **🛠️ Technologies Used**
- **Frontend**: React.js  
- **Backend**: Python, AWS Lambda  
- **API Data Source**: RobotEvents API  
- **Automation**: AWS EventBridge  
- **Hosting**: AWS S3 + CloudFront  

---

## **📸 Link**
🚀 _https://skills.bmcc.cloud_

---

