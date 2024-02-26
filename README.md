**Abstract**
The Internet of Things (IoT) is increasingly gaining significance in the global technological landscape, characterized by a complex and dynamic network of interconnected devices ranging from smart home appliances to highly specialized industrial sensors. With over 30 billion connected devices worldwide, IoT plays a significant role in the digital economy, transforming sectors such as healthcare and manufacturing. This rapid expansion is revolutionizing how systems are designed, developed, and managed.

In this context, one of the most pressing needs is to ensure that such systems behave as expected and support certain non-functional requirements. To address this need, research has focused on security assurance techniques in general and certification in particular. However, existing certification techniques are not suitable for certifying IoT systems because they are designed for deterministic, low-dynamic environments and assume full knowledge of the system to be certified. This assumption, in particular, falls short in the IoT context, where the system is continuously changing. This makes existing certification techniques obsolete.

The goal of this thesis is the definition, implementation, and experimental evaluation of a certification scheme for IoT systems, building on an existing thesis. For the first time in literature, the proposed scheme supports dynamic non-functional properties, which are discovered continuously without the need to manually specify them at each change, allowing for constant and dynamic monitoring of IoT system characteristics, significantly reducing certification overhead.

The thesis work can be detailed as follows:

1. **State of the Art Study**: The study focused on an in-depth analysis of existing certification techniques, both research and commercial; and the initial thesis and its limitations, particularly the inability to follow IoT system changes and perform targeted re-certification.

2. **Definition of a Complete Certification Scheme**: The certification scheme was formalized, consisting mainly of: i) a Certification Model, guiding certification activities regarding ii) properties concerning the examined system, iii) an evidence collection model underpinning the certification of properties.

3. **Certification Process Definition**: Based on the scheme in point 2, a continuous certification process was defined that certifies a given system given the corresponding Certification Model. Initially, the process performs an exploration phase, where evidence is collected in a targeted manner, i.e., collecting the minimum set of evidence leading to the issuance of a certificate. Subsequently, the Certification Model and the corresponding certificate itself are dynamically adapted with respect to changes occurring in the system.

4. **Experimental Evaluation of the Solution**: The experimental evaluation is based on: i) an extensive set of experimental configurations, generated probabilistically to simulate various typical IoT system scenarios; ii) a performance evaluation focused on the execution times of the certification process; iii) a quality evaluation in terms of the fraction of evidence collected compared to all possible evidence during continuous certification. The results show that execution times are contained, never exceeding 2.6ms; while for quality, the best result occurred in the configuration that collected about 23% of the total possible evidence. This implies a significant reduction in overall overhead.

This thesis work lends itself to future developments. Firstly, through the analysis of results obtained in the experimentation phase, there is the possibility of carrying out targeted optimizations on certain IoT scenarios. Secondly, a new definition of the Certification Model and respective process in relation to multiple heterogeneous properties, in contrast with the approach presented by this thesis, which considers homogeneous properties.










**Overview**
This project is designed to generate, test, extract, and analyze performance data for various system configurations and scenarios. It consists of four main components:

dataset_generator.py: Generates datasets with specific characteristics for testing or analysis.
test_benchmark.py: Utilizes pytest to automate testing and benchmarking of system performance.
extract.py: Extracts and processes JSON data into structured formats for analysis.
explore_PERFORMACE.py: Analyzes and optimizes system performance based on microproperties and configurations.
Getting Started

**Prerequisites**
Python 3.x
Pandas
NumPy
pytest
Installation
Clone the repository to your local machine.
Ensure you have Python 3.x installed along with the required libraries: Pandas, NumPy, and pytest.
Usage
Generating Datasets
bash
Copy code
python dataset_generator.py
This script generates datasets based on predefined configurations and characteristics.

**Running Benchmarks**
bash
Copy code
pytest test_benchmark.py
Automates testing and benchmarking against the generated datasets and explores system performance under various configurations.

**Extracting Data**
bash
Copy code
python extract.py
Loads JSON data and transforms it into a structured format for analysis.

**Exploring Performance**
bash
Copy code
python explore_PERFORMACE.py
Processes and analyzes microproperties to optimize or understand system performance.

**Exploring Quality**
bash
Copy code
python explore_QUALITY.py
Processes and analyzes microproperties to optimize or understand system quality.

**Contributing**
Contributions are welcome! Please feel free to submit pull requests or open issues to discuss potential improvements or features.

**Contacts**
Details on how to contact fede2968@gmail.com for questions or future collaborations. This provides a direct line of communication for support, feedback, or discussions about potential partnerships.

**License**
This project is licensed under the MIT License - see the LICENSE file for details.

