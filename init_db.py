from models import SessionLocal, create_tables, JobDetails

def seed_job_details():
    """Seed job details into the database"""
    db = SessionLocal()
    try:
        # Check if we already have job details
        job_count = db.query(JobDetails).count()
        if job_count > 0:
            print("Job details already exist in the database. Skipping seed.")
            return
        
        # Create sample job details - multiple positions
        jobs = [
            # Job 1
            JobDetails(
                job_title="Software Engineer",
                job_details="""Description:
We are seeking a skilled Software Engineer to design, develop, and maintain software applications. The ideal candidate will write efficient code, troubleshoot issues, and collaborate with teams to deliver high-quality solutions.

Responsibilities:
- Develop, test, and deploy software applications.
- Write clean, maintainable, and scalable code.
- Collaborate with cross-functional teams to define and implement features.
- Troubleshoot and debug issues for optimal performance.
- Stay updated with emerging technologies and best practices.

Qualifications:
- Bachelor's degree in Computer Science or a related field.
- Proficiency in programming languages like Python, Java, or C++.
- Experience with databases, web development, and software frameworks.
- Strong problem-solving skills and attention to detail.
- Ability to work both independently and in a team environment.""",
                skills_requirement="Python, Java, C++, databases, web development, software frameworks",
                education_requirement="Bachelor's degree in Computer Science or related field",
                experience_requirement="2+ years of experience as a Software Engineer",
                additional_requirements="Certifications or special training related to Software Engineering are a plus"
            ),
            
            # Job 2
            JobDetails(
                job_title="Data Scientist",
                job_details="""Job Description:
We are looking for a skilled Data Scientist to analyze complex datasets, develop predictive models, and provide actionable insights. You will collaborate with cross-functional teams to optimize business strategies and drive data-driven decision-making.

Responsibilities:
- Collect, clean, and analyze large datasets.
- Develop and deploy machine learning models.
- Build predictive analytics solutions to improve business outcomes.
- Communicate findings through reports and visualizations.
- Stay updated with advancements in data science and AI.

Qualifications:
- Bachelor's or Master's degree in Data Science, Computer Science, or a related field.
- Proficiency in Python, R, SQL, and machine learning frameworks.
- Experience with data visualization tools like Tableau or Power BI.
- Strong analytical and problem-solving skills.
- Ability to work independently and in a team environment.""",
                skills_requirement="Python, R, SQL, machine learning frameworks, Tableau, Power BI",
                education_requirement="Bachelor's or Master's degree in Data Science, Computer Science, or related field",
                experience_requirement="2+ years of experience as a Data Scientist",
                additional_requirements="Experience with big data technologies and cloud platforms is a plus"
            ),
            
            # Job 3
            JobDetails(
                job_title="Product Manager",
                job_details="""Description:
We are seeking an innovative and strategic Product Manager to lead the development and execution of new products. The ideal candidate will collaborate with cross-functional teams to define product roadmaps, analyze market trends, and ensure successful product launches.

Responsibilities:
- Define product vision and strategy based on market research and customer needs.
- Work closely with engineering, design, and marketing teams to develop and launch products.
- Prioritize features, create roadmaps, and manage product lifecycle.
- Analyze user feedback and data to optimize product performance.
- Ensure alignment between business goals and product development.

Qualifications:
- Bachelor's degree in Business, Computer Science, or a related field.
- Experience in product management, agile methodologies, and market research.
- Strong analytical, leadership, and communication skills.
- Familiarity with project management tools and data-driven decision-making.""",
                skills_requirement="Product management, agile methodologies, market research, analytics",
                education_requirement="Bachelor's degree in Business, Computer Science, or related field",
                experience_requirement="2+ years of experience as a Product Manager",
                additional_requirements="Product management certifications and experience with product analytics are a plus"
            ),
            
            # Job 4
            JobDetails(
                job_title="Cloud Engineer",
                job_details="""Description:
We are looking for a skilled Cloud Engineer to design, implement, and manage cloud-based infrastructure. You will optimize performance, enhance security, and ensure scalability while collaborating with development teams to deploy cloud solutions efficiently.

Responsibilities:
- Design and maintain cloud architecture for high availability and security.
- Automate deployments and manage CI/CD pipelines.
- Monitor cloud systems, troubleshoot issues, and optimize costs.
- Implement security best practices and compliance measures.

Qualifications:
- Bachelor's degree in Computer Science, IT, or related field.
- Experience with cloud platforms like AWS, Azure, or Google Cloud.
- Proficiency in infrastructure-as-code (Terraform, CloudFormation).
- Strong scripting skills in Python, Bash, or PowerShell.""",
                skills_requirement="AWS, Azure, Google Cloud, Terraform, CloudFormation, Python, Bash, PowerShell",
                education_requirement="Bachelor's degree in Computer Science, IT, or related field",
                experience_requirement="2+ years of experience as a Cloud Engineer",
                additional_requirements="AWS, Azure, or Google Cloud certifications are highly valued"
            ),
            
            # Job 5
            JobDetails(
                job_title="Cybersecurity Analyst",
                job_details="""Description:
We are looking for a skilled Cybersecurity Analyst to protect our organization's systems and data from cyber threats. You will monitor networks, analyze security incidents, and implement protective measures to ensure compliance and data integrity.

Responsibilities:
- Monitor and analyze security alerts to detect potential threats.
- Conduct vulnerability assessments and risk analysis.
- Implement security policies, firewalls, and encryption protocols.
- Investigate and respond to security breaches.
- Ensure compliance with cybersecurity regulations and best practices.

Qualifications:
- Bachelor's degree in Cybersecurity, Computer Science, or related field.
- Experience with security tools like SIEM, firewalls, and intrusion detection systems.
- Knowledge of network security, encryption, and risk management.
- Strong analytical and problem-solving skills.
- Certifications like CEH, CISSP, or CompTIA Security+ are a plus.""",
                skills_requirement="SIEM, firewalls, intrusion detection systems, network security, encryption",
                education_requirement="Bachelor's degree in Cybersecurity, Computer Science, or related field",
                experience_requirement="2+ years of experience as a Cybersecurity Analyst",
                additional_requirements="CEH, CISSP, or CompTIA Security+ certifications are highly desired"
            ),
            
            # Job 6
            JobDetails(
                job_title="Machine Learning Engineer",
                job_details="""Description:
We are looking for a skilled Machine Learning Engineer to develop, train, and deploy AI models for real-world applications. You will work with large datasets, optimize algorithms, and collaborate with cross-functional teams to drive innovation.

Responsibilities:
- Develop and optimize machine learning models for various applications.
- Process and analyze large datasets to extract meaningful insights.
- Deploy and maintain AI models in production environments.
- Collaborate with data scientists, engineers, and product teams.
- Stay updated with the latest advancements in AI and ML.

Qualifications:
- Bachelor's or Master's in Computer Science, Data Science, or a related field.
- Proficiency in Python, TensorFlow, PyTorch, and Scikit-learn.
- Experience with data preprocessing, model deployment, and cloud platforms.
- Strong problem-solving skills and analytical mindset.""",
                skills_requirement="Python, TensorFlow, PyTorch, Scikit-learn, data preprocessing, model deployment",
                education_requirement="Bachelor's or Master's in Computer Science, Data Science, or related field",
                experience_requirement="2+ years of experience as a Machine Learning Engineer",
                additional_requirements="Experience with MLOps and production ML systems is a plus"
            ),
            
            # Job 7
            JobDetails(
                job_title="DevOps Engineer",
                job_details="""Description:
We are seeking a skilled DevOps Engineer to streamline development, deployment, and operations. You will be responsible for automating infrastructure, improving CI/CD pipelines, and ensuring system reliability, security, and scalability.

Responsibilities:
- Develop and maintain CI/CD pipelines for seamless deployment.
- Automate infrastructure management using tools like Terraform or Ansible.
- Monitor system performance and ensure high availability.
- Collaborate with development and operations teams to optimize workflows.
- Implement security best practices and ensure compliance.

Qualifications:
- Bachelor's degree in Computer Science, IT, or related field.
- Proficiency in cloud platforms (AWS, Azure, or Google Cloud).
- Experience with containerization (Docker, Kubernetes).
- Strong scripting skills (Python, Bash, or PowerShell).
- Knowledge of configuration management tools (Ansible, Chef, or Puppet).""",
                skills_requirement="AWS, Azure, Google Cloud, Docker, Kubernetes, Python, Bash, PowerShell, Ansible, Chef, Puppet",
                education_requirement="Bachelor's degree in Computer Science, IT, or related field",
                experience_requirement="2+ years of experience as a DevOps Engineer",
                additional_requirements="Certifications in cloud platforms and containerization technologies are a plus"
            ),
            
            # Job 8
            JobDetails(
                job_title="Full Stack Developer",
                job_details="""Description:
We are looking for a skilled Full Stack Developer to design, develop, and maintain web applications. You will work on both frontend and backend development, ensuring seamless user experiences and optimized performance.

Responsibilities:
- Develop and maintain web applications using modern frontend and backend technologies.
- Collaborate with designers and backend engineers to implement new features.
- Optimize application performance and ensure scalability.
- Troubleshoot and debug issues in a fast-paced environment.
- Stay updated with emerging web technologies and best practices.

Qualifications:
- Bachelor's degree in Computer Science or related field (or equivalent experience).
- Proficiency in JavaScript, React, Node.js, and databases (SQL/NoSQL).
- Experience with RESTful APIs, cloud services, and version control (Git).
- Strong problem-solving skills and ability to work in a collaborative team.""",
                skills_requirement="JavaScript, React, Node.js, SQL, NoSQL, RESTful APIs, Git",
                education_requirement="Bachelor's degree in Computer Science or related field (or equivalent experience)",
                experience_requirement="2+ years of experience as a Full Stack Developer",
                additional_requirements="Experience with modern frontend frameworks and cloud services is desirable"
            ),
            
            # Job 9
            JobDetails(
                job_title="Big Data Engineer",
                job_details="""Description:
We are seeking a skilled Big Data Engineer to design, develop, and maintain scalable data pipelines for processing and analyzing large datasets. You will work with distributed computing technologies to optimize data workflows and support data-driven decision-making.

Responsibilities:
- Design and implement data pipelines for large-scale processing.
- Optimize data storage and retrieval for performance and scalability.
- Work with cloud-based and on-premises big data technologies.
- Ensure data security, integrity, and compliance.
- Collaborate with data scientists and analysts to support business needs.

Qualifications:
- Bachelor's/Master's degree in Computer Science, Data Engineering, or related field.
- Experience with Hadoop, Spark, Kafka, and distributed computing.
- Proficiency in SQL, Python, or Scala for data processing.
- Knowledge of cloud platforms like AWS, Azure, or GCP.
- Strong problem-solving and analytical skills.""",
                skills_requirement="Hadoop, Spark, Kafka, distributed computing, SQL, Python, Scala, AWS, Azure, GCP",
                education_requirement="Bachelor's/Master's degree in Computer Science, Data Engineering, or related field",
                experience_requirement="2+ years of experience as a Big Data Engineer",
                additional_requirements="Experience with real-time data processing and data warehousing solutions"
            ),
            
            # Job 10
            JobDetails(
                job_title="AI Researcher",
                job_details="""Description:
We are seeking an innovative AI Researcher to develop cutting-edge AI models and algorithms. You will work on advancing machine learning techniques, optimizing AI systems, and applying research to real-world applications.

Responsibilities:
- Conduct research in AI, deep learning, and NLP.
- Develop and optimize machine learning models.
- Publish findings in top-tier conferences and journals.
- Collaborate with cross-functional teams to integrate AI solutions.
- Stay updated with the latest AI advancements and technologies.

Qualifications:
- Ph.D. or Master's in AI, Machine Learning, or related field.
- Strong programming skills in Python, TensorFlow, or PyTorch.
- Experience with research methodologies and model optimization.
- Excellent problem-solving and analytical skills.""",
                skills_requirement="Python, TensorFlow, PyTorch, deep learning, NLP, research methodologies",
                education_requirement="Ph.D. or Master's in AI, Machine Learning, or related field",
                experience_requirement="2+ years of experience in AI research or similar roles",
                additional_requirements="Publication record in top-tier AI conferences or journals is highly valued"
            ),
            
            # Job 11 - Database Administrator
            JobDetails(
                job_title="Database Administrator",
                job_details="""Description:
We are seeking a skilled Database Administrator to manage, optimize, and secure database systems across our organization. You will ensure high performance, availability, and data integrity while proactively monitoring systems and implementing best practices.

Responsibilities:
- Install, configure, and maintain various database systems.
- Optimize database performance and ensure data security.
- Perform regular backups, recovery testing, and troubleshooting.
- Monitor system health and resolve database issues promptly.
- Implement industry best practices for database design and management.
- Collaborate with development teams to optimize database interactions.

Qualifications:
- Bachelor's degree in Computer Science or related field.
- Proficiency in SQL and major database management systems (MySQL, PostgreSQL, Oracle, or MongoDB).
- Experience in database security, backup strategies, and performance optimization.
- Strong problem-solving and analytical skills.
- Excellent communication and documentation abilities.""",
                skills_requirement="SQL, MySQL, PostgreSQL, Oracle, MongoDB, database security, performance tuning",
                education_requirement="Bachelor's degree in Computer Science or related field",
                experience_requirement="2+ years of experience as a Database Administrator",
                additional_requirements="Oracle, Microsoft SQL Server, or MongoDB certifications are highly valued"
            ),
            
            # Job 12 - Network Engineer
            JobDetails(
                job_title="Network Engineer",
                job_details="""Description:
We are looking for a skilled Network Engineer to design, implement, and maintain our network infrastructure. You will ensure high availability, security, and performance while troubleshooting issues and optimizing connectivity across the organization.

Responsibilities:
- Design and deploy network solutions for optimal performance and reliability.
- Monitor network health and troubleshoot complex connectivity issues.
- Implement robust security measures to protect network integrity.
- Manage firewalls, routers, switches, and VPN systems.
- Ensure compliance with networking best practices and industry standards.
- Document network configurations and maintain up-to-date topology diagrams.

Qualifications:
- Bachelor's degree in Computer Science, IT, or a related field.
- Strong knowledge of networking protocols and technologies (TCP/IP, DNS, DHCP, VLANs).
- Experience with firewalls, routers, switches, and enterprise networking solutions.
- Proficiency in Cisco, Juniper, or similar networking technologies.
- Excellent problem-solving skills and ability to work under pressure.
- Strong communication and teamwork abilities.""",
                skills_requirement="TCP/IP, DNS, DHCP, VLANs, Cisco, Juniper, firewalls, routing, switching",
                education_requirement="Bachelor's degree in Computer Science, IT, or related field",
                experience_requirement="2+ years of experience as a Network Engineer",
                additional_requirements="CCNA, CCNP, or other networking certifications are highly desired"
            ),
            
            # Job 13 - Software Architect
            JobDetails(
                job_title="Software Architect",
                job_details="""Description:
We are seeking an experienced Software Architect to design and oversee the development of scalable, high-performance software solutions. You will define system architecture, establish technical standards, and collaborate with development teams to deliver efficient, secure, and maintainable applications.

Responsibilities:
- Design and implement robust, scalable software architectures.
- Guide development teams in best coding practices and design patterns.
- Ensure scalability, security, and performance of applications.
- Conduct architectural reviews and optimize system workflows.
- Evaluate new technologies and recommend appropriate solutions.
- Collaborate with stakeholders to align technical solutions with business needs.

Qualifications:
- Bachelor's/Master's degree in Computer Science or related field.
- Strong expertise in software design patterns and system architecture.
- Proficiency in cloud computing, microservices, and DevOps practices.
- Experience with multiple programming languages like Java, Python, or C++.
- Excellent problem-solving, leadership, and communication skills.
- Proven track record of successful software architecture implementation.""",
                skills_requirement="Software design patterns, system architecture, cloud computing, microservices, Java, Python, C++",
                education_requirement="Bachelor's/Master's degree in Computer Science or related field",
                experience_requirement="5+ years of experience in software development with at least 2 years in architecture roles",
                additional_requirements="AWS/Azure certifications and experience with large-scale distributed systems"
            ),
            
            # Job 14 - Blockchain Developer
            JobDetails(
                job_title="Blockchain Developer",
                job_details="""Description:
We are looking for a talented Blockchain Developer to design, develop, and maintain blockchain-based applications and solutions. You will work with smart contracts, decentralized applications (DApps), and cryptographic protocols to build innovative and secure blockchain solutions.

Responsibilities:
- Develop and deploy secure smart contracts and blockchain applications.
- Optimize blockchain infrastructure for performance and scalability.
- Integrate blockchain solutions with existing systems and applications.
- Implement security best practices in blockchain implementations.
- Research and evaluate emerging blockchain technologies and trends.
- Collaborate with cross-functional teams to deliver blockchain solutions.

Qualifications:
- Bachelor's degree in Computer Science, Information Technology, or a related field.
- Proficiency in Solidity, Ethereum, Hyperledger, or other blockchain platforms.
- Experience with cryptography, smart contracts, and decentralized applications.
- Understanding of blockchain consensus mechanisms and network architecture.
- Strong problem-solving skills and knowledge of distributed systems.
- Experience with web3.js, ethers.js, or similar blockchain libraries.""",
                skills_requirement="Solidity, Ethereum, Hyperledger, smart contracts, cryptography, web3.js, JavaScript",
                education_requirement="Bachelor's degree in Computer Science, IT, or related field",
                experience_requirement="2+ years of experience in blockchain development",
                additional_requirements="Certified Blockchain Developer credential and experience with DeFi protocols"
            ),
            
            # Job 15 - IT Project Manager
            JobDetails(
                job_title="IT Project Manager",
                job_details="""Description:
We are seeking an experienced IT Project Manager to oversee technical projects from planning to execution, ensuring timely delivery within scope and budget. You will collaborate with cross-functional teams, manage project risks, and implement best practices to ensure successful project completion.

Responsibilities:
- Define project scope, objectives, and deliverables in collaboration with stakeholders.
- Develop detailed project plans, timelines, budgets, and resource requirements.
- Coordinate between cross-functional teams and manage stakeholder expectations.
- Identify, assess, and mitigate risks to ensure smooth project execution.
- Monitor project progress and provide regular status updates to stakeholders.
- Lead project reviews and implement continuous improvement strategies.

Qualifications:
- Bachelor's degree in IT, Computer Science, Business, or related field.
- Proven experience in managing complex IT projects from initiation to completion.
- Knowledge of Agile, Scrum, and traditional project management methodologies.
- Strong leadership, communication, and problem-solving skills.
- Ability to manage multiple projects simultaneously in a fast-paced environment.
- Excellent documentation and reporting skills.""",
                skills_requirement="Agile, Scrum, Waterfall, JIRA, MS Project, stakeholder management, risk management",
                education_requirement="Bachelor's degree in IT, Computer Science, Business, or related field",
                experience_requirement="3+ years of experience in IT project management",
                additional_requirements="PMP, PRINCE2, or Agile certifications are highly desirable"
            ),
            
            # Job 16 - Business Intelligence Analyst
            JobDetails(
                job_title="Business Intelligence Analyst",
                job_details="""Description:
We are looking for a detail-oriented Business Intelligence Analyst to analyze complex business data, identify trends, and generate actionable insights. You will develop reports and interactive dashboards to help stakeholders make data-driven decisions and improve business performance.

Responsibilities:
- Collect, process, and analyze large datasets to extract valuable business insights.
- Design and develop interactive dashboards and reports using BI tools.
- Collaborate with departments to understand their data needs and improve decision-making.
- Identify patterns, trends, and correlations in complex datasets.
- Ensure data accuracy, consistency, and integrity in all reporting.
- Present findings and recommendations to stakeholders at all levels.

Qualifications:
- Bachelor's degree in Data Science, Business Analytics, Statistics, or a related field.
- Proficiency in SQL, Power BI, Tableau, or similar business intelligence tools.
- Strong analytical thinking and problem-solving abilities.
- Experience in data visualization, statistical analysis, and data modeling.
- Excellent communication skills for presenting complex data simply.
- Ability to translate business requirements into analytical frameworks.""",
                skills_requirement="SQL, Power BI, Tableau, data visualization, statistical analysis, Excel advanced functions",
                education_requirement="Bachelor's degree in Data Science, Business Analytics, Statistics, or related field",
                experience_requirement="2+ years of experience in business intelligence or data analysis",
                additional_requirements="Tableau certifications and experience with data warehousing concepts"
            ),
            
            # Job 17 - Robotics Engineer
            JobDetails(
                job_title="Robotics Engineer",
                job_details="""Description:
We are seeking an innovative Robotics Engineer to design, develop, and optimize robotic systems for automation and intelligent applications. You will work on the integration of hardware and software, motion control systems, and AI-driven solutions to create cutting-edge robotic technologies.

Responsibilities:
- Design, build, and test robotic systems for industrial or research applications.
- Develop software algorithms for navigation, control, and automation.
- Integrate sensors, actuators, and AI-based decision-making systems.
- Troubleshoot and optimize robotic performance and reliability.
- Collaborate with cross-functional teams on robotics projects.
- Stay updated with emerging robotics technologies and advancements.

Qualifications:
- Bachelor's or Master's degree in Robotics, Mechanical Engineering, or related field.
- Proficiency in C++, Python, and ROS (Robot Operating System).
- Experience with embedded systems, motion planning, and control theory.
- Knowledge of AI and machine learning applications in robotics.
- Strong analytical and problem-solving skills.
- Ability to work collaboratively in a research and development environment.""",
                skills_requirement="C++, Python, ROS, embedded systems, motion planning, control systems, AI integration",
                education_requirement="Bachelor's or Master's degree in Robotics, Mechanical Engineering, or related field",
                experience_requirement="2+ years of experience in robotics development",
                additional_requirements="Experience with computer vision and autonomous systems"
            ),
            
            # Job 18 - Embedded Systems Engineer
            JobDetails(
                job_title="Embedded Systems Engineer",
                job_details="""Description:
We are looking for a skilled Embedded Systems Engineer to design and develop software for embedded systems and devices. You will work with microcontrollers, real-time operating systems, and low-level programming to build reliable, efficient, and innovative solutions across various industries.

Responsibilities:
- Develop, test, and optimize embedded software and firmware for electronic devices.
- Collaborate with hardware engineers to ensure seamless hardware-software integration.
- Debug and troubleshoot complex real-time system issues.
- Optimize power consumption, performance, and resource utilization.
- Write clean, maintainable, and well-documented code.
- Stay updated with emerging technologies in embedded systems development.

Qualifications:
- Bachelor's degree in Electrical Engineering, Computer Engineering, or related field.
- Proficiency in C/C++, assembly language, and embedded Linux.
- Experience with microcontrollers (ARM, PIC, AVR), RTOS, and debugging tools.
- Knowledge of communication protocols (I2C, SPI, UART, CAN).
- Strong problem-solving and analytical skills.
- Ability to read schematics and work closely with hardware teams.""",
                skills_requirement="C/C++, assembly, embedded Linux, ARM, PIC, AVR, RTOS, I2C, SPI, UART, CAN",
                education_requirement="Bachelor's degree in Electrical Engineering, Computer Engineering, or related field",
                experience_requirement="2+ years of experience in embedded systems development",
                additional_requirements="Experience with IoT devices and low-power design techniques"
            ),
            
            # Job 19 - Quality Assurance Engineer
            JobDetails(
                job_title="Quality Assurance Engineer",
                job_details="""Description:
We are seeking a detail-oriented Quality Assurance Engineer to ensure the reliability and performance of our software applications. You will design and implement comprehensive test strategies, identify defects, and collaborate with development teams to deliver high-quality software products.

Responsibilities:
- Develop and execute detailed test plans, cases, and scripts.
- Identify, document, and track software defects to ensure timely resolution.
- Design and implement automated testing frameworks to improve efficiency.
- Perform functional, regression, performance, and security testing.
- Collaborate with developers to enhance software quality and user experience.
- Participate in Agile ceremonies and provide quality metrics and reports.

Qualifications:
- Bachelor's degree in Computer Science, Engineering, or related field.
- Experience with testing tools like Selenium, JUnit, TestNG, or Cypress.
- Knowledge of test management systems and bug tracking tools.
- Strong analytical and problem-solving skills.
- Understanding of software development lifecycle (SDLC) and Agile methodologies.
- Excellent communication and teamwork abilities.""",
                skills_requirement="Selenium, JUnit, TestNG, Cypress, test automation, API testing, Agile methodologies",
                education_requirement="Bachelor's degree in Computer Science, Engineering, or related field",
                experience_requirement="2+ years of experience in software testing or quality assurance",
                additional_requirements="ISTQB certification and experience with CI/CD pipelines"
            ),
            
            # Job 20 - UX/UI Designer
            JobDetails(
                job_title="UX/UI Designer",
                job_details="""Description:
We are seeking a creative and user-focused UX/UI Designer to create intuitive and visually appealing digital experiences. You will collaborate with product managers, developers, and stakeholders to design user-friendly interfaces that balance aesthetic appeal with functionality.

Responsibilities:
- Design wireframes, prototypes, and UI elements based on user research and requirements.
- Conduct user research, usability testing, and analyze feedback to refine designs.
- Create user flows, journey maps, and information architecture.
- Develop and maintain design systems and style guides.
- Collaborate with development teams to ensure accurate implementation.
- Stay updated with design trends, tools, and best practices.

Qualifications:
- Bachelor's degree in Design, Human-Computer Interaction, or a related field.
- Proficiency in design tools like Figma, Adobe XD, or Sketch.
- Strong portfolio demonstrating UX/UI design skills and problem-solving.
- Understanding of user experience principles and front-end technologies.
- Excellent visual design skills with attention to detail.
- Strong communication and presentation abilities.""",
                skills_requirement="Figma, Adobe XD, Sketch, wireframing, prototyping, user research, visual design",
                education_requirement="Bachelor's degree in Design, Human-Computer Interaction, or related field",
                experience_requirement="2+ years of experience in UX/UI design",
                additional_requirements="Experience with design systems and mobile app design"
            ),
            
            # Job 21 - Data Science Fresher (improved)
            JobDetails(
                job_title="Data Science Fresher",
                job_details="""Description:
We're looking for enthusiastic and talented entry-level Data Scientists to join our growing team. This role offers opportunities to work on real-world data problems while developing your skills in machine learning, data analysis, and business intelligence.

Responsibilities:
- Assist in collecting, cleaning, and analyzing datasets.
- Help develop and improve machine learning models and algorithms.
- Contribute to data visualization and presentation of insights.
- Collaborate with senior data scientists on various projects.
- Learn and apply best practices in data science and analytics.

Qualifications:
- Bachelor's or Master's in Computer Science, Data Science, Statistics, Mathematics, AI, or related field.
- Programming skills in Python, R, or SQL.
- Basic understanding of machine learning concepts and statistical analysis.
- Familiarity with data visualization tools like Matplotlib, Seaborn, or Tableau.
- Strong analytical thinking and problem-solving abilities.
- Excellent communication skills and eagerness to learn.""",
                skills_requirement="Programming: Python, R, SQL. Machine Learning: Supervised & Unsupervised learning. Data Visualization: Matplotlib, Seaborn, Tableau. Big Data: Hadoop, Spark, AWS, GCP. Soft Skills: Analytical thinking, problem-solving, communication skills.",
                education_requirement="Bachelor's or Master's in Computer Science, Data Science, Statistics, Mathematics, AI, or related field. Preferred certifications: Coursera, Udacity, IBM Data Science, Google Data Analytics.",
                experience_requirement="0-2 years experience. Preferred: Internship, freelance projects, research work, Kaggle competitions. Bonus: Open-source contributions or hackathons.",
                additional_requirements="Strong passion for data-driven decision-making. Ability to adapt to new technologies. Familiarity with cloud platforms (AWS, Azure, GCP) is an advantage."
            )
        ]
        
        # Add all jobs to the database
        for job in jobs:
            db.add(job)
        
        db.commit()
        print(f"Added {len(jobs)} job details successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding job details: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    create_tables()
    
    # Seed job details
    seed_job_details()
    
    print("Database initialization complete.") 