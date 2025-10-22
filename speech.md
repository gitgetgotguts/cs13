### **Complete Speaker Scripts for the Full Presentation**

**Slide 1: Host Company: JUMBO BAGS**
"Good morning. My summer internship was conducted at JUMBO BAGS, a Tunisian industrial company established in 2017. They specialize in manufacturing the large polypropylene bags, known as Big Bags, used in many industries."

**Slide 2: The Manufacturing Workflow**
"To understand the context of my work, I first studied the company's entire manufacturing workflow. It's a multi-stage process that combines both automated and manual tasks. My analysis, which I'll present next, focused specifically on this key step: the Automated Cutting."

**Slide 3: Control System: The Human-Machine Interface (HMI)**
"The first part of my control system analysis focused on the Human-Machine Interface, or HMI. This touchscreen is the brain of the machine, where the operator inputs all the digital instructions for a specific job. This includes critical parameters like the precise cutting length, the batch size for collection, and the machine's operating speed."

**Slide 4: Control System: The Physical Control Panel**
"The second part of the analysis was the physical control panel, which is used to execute the program and monitor the machine. It includes the essential functions for operation: an emergency stop for safety, a switch to select the mode, and the start/stop buttons. Crucially, it also has components for process monitoring, like the temperature controller. Here, the operator sets a target value (SV), and the machine maintains the actual value (PV), which is a perfect example of real-time process control to ensure a quality cut."

**Slide 5: The Automated Cutter: Deduced Logic**
"By combining my analysis of both the HMI and the control panel, I was able to map out the machine's complete logic. It's more than a simple loop; it's a nested process designed for human interaction. The inner loop cuts pieces until a batch is finished. Then, the machine pauses and waits for the operator to collect the parts and press START again. This entire cycle repeats until the total production goal is met. This shows a clear, programmed collaboration between the automated system and the operator."

**Slide 6: The Challenge: A Broken Inventory System**
"In addition to analyzing the cutter, I was also assigned a practical mission: to fix the company's broken spare parts inventory. The core problem was a complete disconnect between the digital records, which were spread across 15 messy files, and the physically disorganized parts. There was no link between them, which caused major delays for the maintenance team."

**Slide 7: The Plan: A Systematic Rebuild**
"Before starting, I laid out a clear two-phase plan. My main objective was to create a 'single source of truth' where the digital data perfectly matched the physical reality. Phase one would be to fix the digital mess by creating one clean master list. Phase two would be to organize the physical parts and then link each item's location back to that master list."

**Slide 8: Phase 1: Building the Master Parts Database**
"To execute phase one, my first step was to build a complete master parts database from scratch. The information I needed was scattered everywhere—not just in 15 old internal files, but also across various supplier spreadsheets. So, I gathered all these different files and wrote a Python script using the Pandas library to automatically merge, clean, and centralize all the data. This created a single, comprehensive master list that we could trust as the foundation for the entire system."

**Slide 9: Phase 2: Linking Digital Data to the Physical World**
"For phase two, I needed to count every part and, crucially, link it to a physical location. I developed a custom tool to make this efficient. I would organize a drawer, give it a number like 'Box 27', then use my tool to find the part, enter the quantity I counted, and add that box number. This created the vital link between the digital record and its exact spot on the shelf."

**(You will need a final conclusion slide after this. Here is a suggestion for it.)**

**Slide 10: Conclusion & Impact**
"To summarize, my internship had two main components. First, the technical analysis of the automated cutter, which allowed me to apply my knowledge of control systems in a real-world setting. Second, the inventory project, which was a hands-on mission from planning and data automation with Python to final implementation. This project resulted in a significant and measurable improvement for the maintenance team, reducing part search time from over 30 minutes to just two. It was an invaluable experience that bridged the gap between academic theory and practical engineering. Thank you for your attention, and I would be happy to answer any questions."
