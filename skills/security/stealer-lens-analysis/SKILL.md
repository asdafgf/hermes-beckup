---
name: stealer-lens-analysis
description: A Hermes Agent skill to analyze stealer logs using LLM and AI.
version: 1.0
category: security
source: https://youtu.be/3j4jzCU0Kwc
tags:
  - cybersecurity
  - threat-intelligence
  - LLM
  - AI
body: |
  ## Introduction

  In this guide, we will explore how to use a Hermes Agent skill to analyze stealer logs using Large Language Models (LLMs) and Artificial Intelligence (AI). This skill is designed to help cybersecurity analysts quickly understand the infection process behind stealer malware by automating the analysis of complex log data.

  ## What are Stealer Logs?

  Stealer logs are the product of info-stealer malware, capturing the entire identity of a user from a compromised device. These logs include sensitive information such as passwords, files, browsing histories, and software processes. Analyzing these logs manually can be time-consuming and complex.

  ## The Genesis of Stealer Lens

  Estelle Roulin, a threat intelligence researcher at Flare, developed the concept of "Stealer Lens" to address this challenge. By using LLMs and AI, Stealer Lens automates the analysis process, allowing analysts to quickly identify how an infection occurred and gather relevant evidence.

  ## How Stealer Lens Works

  The Stealer Lens skill works as follows:

  1. **Input**: Provide raw stealer logs.
  2. **Analysis**: The LLM processes the log data using a human-like logic, identifying suspicious software names, processes, and browsing histories.
  3. **Output**: Receive detailed analysis results, including evidence of how the infection occurred.

  ## Key Features

  - **Automated Analysis**: Reduces manual analysis time significantly.
  - **Human-Like Logic**: Mimics human analysts' decision-making process.
  - **Cross-Referencing**: Cross-references browsing history with software installed to identify anomalies.
  - **Avoids Hallucination**: Ensures accurate and reliable results.

  ## Example Usage

  To use the Stealer Lens skill, follow these steps:

  1. Collect stealer logs from a compromised device.
  2. Input the logs into the Hermes Agent skill.
  3. Review the automated analysis to understand the infection process and gather evidence.

  ## Conclusion

  The Stealer Lens skill is a powerful tool for cybersecurity analysts, leveraging LLMs and AI to automate the complex task of analyzing stealer logs. By automating this process, analysts can save time and focus on more critical tasks, ensuring faster and more accurate threat detection and response.