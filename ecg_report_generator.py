import os 
def generate_ecg_html_report(
    HR, PR, QRS, QT, QTc, ST,
        test_name, date_time,
        first_name, last_name, age, gender,
        abnormal_report, text, obstext, qrstext,
        uId, testId, dataId,
        lead_img_paths = {
            "I": "lead_I.png",
            "II": "lead_II.png",
            "III": "lead_III.png",
            "aVR": "lead_aVR.png",
            "aVL": "lead_aVL.png",
            "aVF": "lead_aVF.png",
            "V1": "lead_V1.png",
            "V2": "lead_V2.png",
            "V3": "lead_V3.png",
            "V4": "lead_V4.png",
            "V5": "lead_V5.png",
            "V6": "lead_V6.png"
        },
        QRS_axis = None
    ):


        def to_float(val):
            try:
               return float(val)
            except Exception:
               return 0

        HR = to_float(HR)
        PR = to_float(PR)
        QRS = to_float(QRS)
        QT = to_float(QT)
        QTc = to_float(QTc)
        ST = to_float(ST)
    
        html = """
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    font-size: 14px;
                    color: #000;
                }
                h1 {
                    text-align: center;
                    font-size: 220px;
                    margin-top: 20px;
                }
                .section-title {
                    font-size: 400px;
                    font-weight: bold;
                    color: #1f75cb;
                    border-bottom: 1px solid #ccc;
                    padding-bottom: 4px;
                    margin-top: 10px;
                    margin-bottom: 10px;
                }
                .info-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 5px 20px;
                    font-size: 140px;
                }
                .two-col-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 140px;
                }
                .two-col-table td {
                    padding: 3px 0;
                    vertical-align: top;
                }
                .two-col-table .label {
                    width: 75%;
                }
                .two-col-table .value {
                    width: 25%;
                    text-align: right;
                    padding-right: 300px;
                }
                .conclusion-box {
                    border: 1px solid #000;
                    padding: 10px;
                    margin-top: 10px;
                    min-height: 550px;
                    font-size: 140px;
                }
                .note {
                    font-size: 120px;
                    margin-top: 8px;
                    margin-bottom: 550px;
                }             
                                
                .header {
                display: flex;
                justify-content: space-between;
                font-size: 140px;
                margin-bottom: 10px;
            }
            .ecg-section {
                margin-bottom: 40px;
            }
            .ecg-title {
                color: #2F80ED;
                font-size: 140px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .ecg-info {
                display: flex;
                justify-content: space-between;
                font-size: 120px;
                margin-bottom: 5px;
            }
            .ecg-image {
                border: 2px solid #999;
                width: 100%;
                height: auto;
                margin-top: 20px;
            }
            .ecg_two{
                margin-bottom: 550px;
            }
            .page-break {
              page-break-before: always;
            }
            .header-cell{
                font-size: 120px;
            }
            .big-table td, .big-table th {
                font-size: 120px;       /* Large text */
                padding: 40px 20px;     /* Adds space inside cell (top/bottom 40px, left/right 20px) */
                text-align: center;     /* Keep text centered */
                vertical-align: middle; /* Align vertically in middle */
            }
            td, th {
                border: 1px solid #ddd; 
                font-size: 120px;       /* Adds a light border around cells */
                }
            </style>
        </head>
        <body>
            <h1>ECG Report</h1>

            <div class="section-title">Basic Information</div>
            <hr style="margin-top:0; margin-bottom:0;">
            <div class="info-grid">
                <div>Name : garymc2</div>
                <div>Gender : Male</div>
                <div>Age : 72</div>
                <div>Recording Time: 2023-07-24 09:50:22  -- </div>
                <div>2023-07-24 15:43:52</div>
                <div>Total Time: 5h53m30s</div>
            </div>

            <div class="section-title">Report Overview</div>
            <hr style="margin-top:0; margin-bottom:0;">
            <table class="two-col-table">
                <tr><td class="label">Total Number of Heartbeats (beats):</td><td class="value">4833</td></tr>
                <tr><td class="label">Percentage of Atrial Flutter and Atrial Fibrillation:</td><td class="value">0</td></tr>
                <tr><td class="label">Maximum Heart Rate:</td><td class="value">136 bpm 14:55:56</td></tr>
                <tr><td class="label">Minimum Heart Rate:</td><td class="value">74 bpm 15:14:38</td></tr>
                <tr><td class="label">Average Heart Rate:</td><td class="value">88 bpm</td></tr>
            </table>

            <div class="section-title">Supraventricular Rhythm</div>
            <hr style="margin-top:0; margin-bottom:0;">
            <table class="two-col-table">
                <tr><td class="label">Total Number of Supraventricular Heart Beats:</td><td class="value">362</td></tr>
                <tr><td class="label">Number of PAC:</td><td class="value">340</td></tr>
                <tr><td class="label">Couplet of PAC:</td><td class="value">3</td></tr>
                <tr><td class="label">Supraventricular Bigeminy (Paroxysmal):</td><td class="value">0</td></tr>
                <tr><td class="label">Supraventricular Trigeminy (Paroxysmal):</td><td class="value">19</td></tr>
                <tr><td class="label">Supraventricular Tachycardia:</td><td class="value">3</td></tr>
                <tr><td class="label">Maximum Duration of Supraventricular Tachycardia(s):</td><td class="value">2.00</td></tr>
                <tr><td class="label">The Longest Time of Supraventricular Tachycardia Happened:</td><td class="value">15:13:03</td></tr>
            </table>

            <div class="section-title">Ventricular Rhythm</div>
            <hr style="margin-top:0; margin-bottom:0;">
            <table class="two-col-table">
                <tr><td class="label">Total Number of Ventricular Heart Beats:</td><td class="value">0</td></tr>
                <tr><td class="label">Number of PVC:</td><td class="value">0</td></tr>
                <tr><td class="label">Couplet of PVC:</td><td class="value">0</td></tr>
                <tr><td class="label">Ventricular Bigeminy (Paroxysmal):</td><td class="value">0</td></tr>
                <tr><td class="label">Ventricular Trigeminy (Paroxysmal):</td><td class="value">0</td></tr>
                <tr><td class="label">Ventricular Tachycardia:</td><td class="value">0</td></tr>
                <tr><td class="label">Maximum Duration of Ventricular Tachycardia (s):</td><td class="value">0.00</td></tr>
                <tr><td class="label">The Longest Time of Ventricular Tachycardia Happened:</td><td class="value"></td></tr>
            </table>
                        
            <div style="page-break-before: always;"></div>
            
            <div class="section-title">HRV</div>
            <hr style="margin-top:0; margin-bottom:0;">
            <table class="two-col-table">
                <tr><td class="label">SDNN:</td><td class="value">118.74 ms</td></tr>
                <tr><td class="label">RMSSD:</td><td class="value">86.43 ms</td></tr>
                <tr><td class="label">SDANN:</td><td class="value">88.05 ms</td></tr>
                <tr><td class="label">SDSSD:</td><td class="value">76.82 ms</td></tr>
                <tr><td class="label">PNN50:</td><td class="value">19.20 %</td></tr>
                <tr><td class="label">TINN:</td><td class="value">28.52</td></tr>
                <tr><td class="label">LF:</td><td class="value">3279.63 ms²</td></tr>
                <tr><td class="label">HF:</td><td class="value">123.12 ms²</td></tr>
                <tr><td class="label">VLF:</td><td class="value">3352638.12 ms²</td></tr>
                <tr><td class="label">ASDNN:</td><td class="value">69.08</td></tr>
            </table>
            
            
            <br>

            <div class="section-title">ECG Report Conclusion</div>
            <hr style="margin-top:0; margin-bottom:0;">
            <div class="info-grid">
                <div>Name : garymc2</div> &nbsp;&nbsp;&nbsp;
                <div>Gender : male</div> &nbsp;&nbsp;&nbsp;
                <div>Age : 72</div>
            </div>
            <div class="conclusion-box">
                1. Sinus Rhythm<br>
                2. PAC (Premature Supraventricular Contraction)<br>
                3. Couplet of PAC<br>
                4. PAC Trigeminy<br>
                5. Supraventricular Tachycardia
            </div>
            
            <div class="note" style="margin-top: 50px;">
            <h3 style="color: red; font-size:100px">Note:</h3> 
                1. Due to the sporadic and transient nature of ECG events, it is normal for each measurement result to be different.<br>
                It is recommended to increase the frequency of monitoring and capture incidents on time.<br>
                2. The results of this analysis are only for reference in daily heart health monitoring; they cannot replace the medical diagnosis results and cannot be used for clinical diagnosis and treatment.
            </div>  
            
            <div style="page-break-before: always;"></div>        
                  
                        
            <!-- Hourly Statistics Table of ECG Data -->
            <h2 style="color:#2E75B6; font-family: Arial, sans-serif;">Hourly Statistics Table of ECG Data</h2>
            <hr style="margin-top:0; margin-bottom:0;">

            <p style="font-family: Arial, sans-serif; font-size: 140px; font-weight: bold;">
                Name : <span style="font-size: 120px; font-weight: normal;">garymc2</span> &nbsp;&nbsp;&nbsp;
                Gender : <span style="font-size: 120px; font-weight: normal;">male</span> &nbsp;&nbsp;&nbsp;
                Age : <span style="font-size: 120px; font-weight: normal;">72</span>
            </p>
            
            <p style="font-family: Arial, sans-serif; font-size: 140px;">
                <strong style="font-size: 120px;">Time:</strong> 2023-07-24 09:50:22 &nbsp;&nbsp; -- &nbsp;&nbsp; 2023-07-24 15:43:52
            </p>

            <table border="1" cellspacing="0" cellpadding="10" 
                style="border-collapse: collapse; 
                       font-family: Arial, sans-serif; 
                       font-size: 120px; 
                       text-align: center; 
                       margin-bottom: 550px; 
                       width: 100%; 
                       table-layout: fixed;">
                <tbody style="background-color: #F2F2F2; height: 80px; font-size: 120px; font-weight: bold;">
                    <tr>
                        <th rowspan="2" class="header-cell" style="white-space: nowrap;">Time<br>HH:MM</th>
                        <th rowspan="2" class="header-cell" style="white-space: nowrap;">Beats<br>(times)</th>
                        <th colspan="3" class="header-cell" style="white-space: nowrap;">Heart Rate</th>
                        <th colspan="6" class="header-cell" style="white-space: nowrap;">Ventricular</th>
                        <th colspan="6" class="header-cell" style="white-space: nowrap;">Atrial</th>
                        <th colspan="2" class="header-cell" style="white-space: nowrap;">Bradycardia</th>
                    </tr>
                    <tr>
                        <th>AVG</th>
                        <th>Min</th>
                        <th>Max</th>
                        <th>Total</th>
                        <th>PVC</th>
                        <th>Couplet</th>
                        <th>Runs</th>
                        <th>Bigeminy</th>
                        <th>Trigeminy</th>
                        <th>Total</th>
                        <th>PAC</th>
                        <th>Couplet</th>
                        <th>Runs</th>
                        <th>Bigeminy</th>
                        <th>Trigeminy</th>
                        <th>Duration</th>
                        <th>Count</th>
                    </tr>
                </tbody>
                <tbody>
                    <tr style="height: 40px; font-size: 120px; ">
                        <td>09:50</td><td>17</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td>
                    </tr>
                    <tr style="height: 40px; font-size: 120px;">
                        <td>10:00</td><td>196</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td>
                    </tr>
                    <tr style="height: 40px; font-size: 120px;">
                        <td>11:00</td><td>155</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td>
                    </tr>
                    <tr style="height: 40px; font-size: 120px;">
                        <td>12:00</td><td>146</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td>
                    </tr>
                    <tr style="height: 40px; font-size: 120px;">
                        <td>13:00</td><td>66</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>0</td>
                    </tr>
                    <tr style="height: 40px; font-size: 120px;">
                        <td>14:00</td><td>505</td><td>99</td><td>80</td><td>136</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>38</td><td>34</td><td>0</td><td>1</td><td>0</td><td>1</td>
                        <td>0</td>
                    </tr>
                    <tr style="height: 40px; font-size: 120px;">
                        <td>15:00</td><td>3748</td><td>86</td><td>74</td><td>126</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>324</td><td>306</td><td>3</td><td>2</td><td>0</td><td>18</td>
                        <td>0</td>
                    </tr>
                    <tr style="height: 50px; font-weight: bold; font-size: 120px;">
                        <td>Total</td><td>4833</td><td>88</td><td>74</td><td>136</td>
                        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
                        <td>362</td><td>340</td><td>3</td><td>3</td><td>0</td><td>19</td>
                        <td>0</td>
                    </tr>
                </tbody>
            </table>
            <div class="note" style="margin-top: 10px;">
            <h3 style="color: red; font-size:100px">Note:</h3> 
                1. Due to the sporadic and transient nature of ECG events, it is normal for each measurement result to be different.<br>
                It is recommended to increase the frequency of monitoring and capture incidents on time.<br>
                2. The results of this analysis are only for reference in daily heart health monitoring; they cannot replace the medical diagnosis results and cannot be used for clinical diagnosis and treatment.
            </div> 
        
        
            <!-- PAC Trigeminy Section -->
            <div class="ecg-section">
                <div class="ecg-title">PAC Trigeminy</div>
                <div class="ecg-info">
                    <span>Time: 2023-07-24 14:58:57</span>
                    <span>Gain: 10 mm/mV</span>
                    <span>Speed: 25 mm/s</span>
                </div>
                <img src="heart_beat.png" alt="PAC Trigeminy ECG" class="ecg-image">
            </div>

            <!--  Couplet of PAC Section -->
            <div class="ecg-section ecg_two">
                <div class="ecg-title"> Couplet of PAC</div>
                <div class="ecg-info">
                    <span>Time: 2023-07-24 14:56:39</span>
                    <span>Gain: 10 mm/mV</span>
                    <span>Speed: 25 mm/s</span>
                </div>
                <img src="heart_beat.png" alt="Supraventricular Tachycardia ECG" class="ecg-image">
            </div>
            
            
            
            
            
            
            <!-- PAC(Premature Supraventricular Contraction) Section -->
            <div class="ecg-section">
                <div class="ecg-title">PAC(Premature Supraventricular Contraction)</div>
                <div class="ecg-info">
                    <span>Time: 2023-07-24 14:58:57</span>
                    <span>Gain: 10 mm/mV</span>
                    <span>Speed: 25 mm/s</span>
                </div>
                <img src="heart_beat.png" alt="PAC Trigeminy ECG" class="ecg-image">
            </div>

            <!-- Supraventricular Tachycardia Section -->
            <div class="ecg-section ecg_two">
                <div class="ecg-title">Supraventricular Tachycardia</div>
                <div class="ecg-info">
                    <span>Time: 2023-07-24 14:56:39</span>
                    <span>Gain: 10 mm/mV</span>
                    <span>Speed: 25 mm/s</span>
                </div>
                <img src="heart_beat.png" alt="Supraventricular Tachycardia ECG" class="ecg-image">
            </div>
            
            
            
            
            
            

            <!-- PAC Trigeminy Section -->
            <div class="ecg-section">
                <div class="ecg-title">PAC Trigeminy</div>
                <div class="ecg-info">
                    <span>Time: 2023-07-24 14:58:57</span>
                    <span>Gain: 10 mm/mV</span>
                    <span>Speed: 25 mm/s</span>
                </div>
                <img src="heart_beat.png" alt="PAC Trigeminy ECG" class="ecg-image">
            </div>

            <!-- Supraventricular Tachycardia Section -->
            <div class="ecg-section ecg_two">
                <div class="ecg-title">Supraventricular Tachycardia</div>
                <div class="ecg-info">
                    <span>Time: 2023-07-24 14:56:39</span>
                    <span>Gain: 10 mm/mV</span>
                    <span>Speed: 25 mm/s</span>
                </div>
                <img src="heart_beat.png" alt="Supraventricular Tachycardia ECG" class="ecg-image">
            </div>
            """

# === dynamically append 12-lead images in groups of 3 ===
        lead_order = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
        if lead_img_paths:
                for i in range(0, len(lead_order), 3):
                    html += '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px;">'
                    for j in range(3):  # 3 columns per row
                        idx = i + j
                        if idx < len(lead_order):
                            lead = lead_order[idx]
                            img_path = lead_img_paths.get(lead)
                            lead_num = idx + 1
                            if img_path and os.path.exists(img_path):
                                html += f'''
        <div class="lead-block" style="padding-bottom:0; min-width:340px; max-width:600px;">
            <div class="lead-label" style="font-size:1.2em;">Lead {lead_num}: {lead}</div>
            <img src="{img_path}" class="lead-img" alt="Lead {lead_num} Graph" height="200" width="550">
        </div>
        '''
                            else:
                                # placeholder when image not found
                                html += f'''
        <div class="lead-block" style="padding-bottom:0; min-width:340px; max-width:600px;">
            <div class="lead-label" style="font-size:1.2em;">Lead {lead_num}: {lead}</div>
            <div style="height:200px; width:550px; border:1px solid #ccc; display:flex; align-items:center; justify-content:center;">
                No image available
            </div>
        </div>
        '''
                    html += '</div>'
                    if i + 3 < len(lead_order):
                        html += '<div class="page-break"></div>'

            # === close html and return ===
        html += """
        </body>
        </html>
                """
        return html
# Generate and save
# html_code = generate_ecg_html_report()
# with open("ecg_report.html", "w", encoding="utf-8") as f:
#     f.write(html_code)

# print("ECG report saved as ecg_report.html")
if __name__ == "__main__":
    # Test run only when executing this file directly
     base_path = os.path.abspath("path_to_images_folder")
     lead_img_paths = {lead: os.path.join(base_path, f"lead_{lead}.png") 
                      for lead in ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]}

     html_code = generate_ecg_html_report(
        HR=80, PR=120, QRS=90, QT=400, QTc=410, ST=0,
        test_name="Test ECG", date_time="2023-07-24 09:50:22",
        first_name="garymc2", last_name="", age=72, gender="male",
        abnormal_report="", text="", obstext="", qrstext="",
        uId="", testId="", dataId="",
        lead_img_paths=lead_img_paths
    )

     with open("ecg_report.html", "w", encoding="utf-8") as f:
        f.write(html_code)

     print("ECG report saved as ecg_report.html")