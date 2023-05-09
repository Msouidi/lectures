#!/bin/bash

# Update the System
echo "[Info] [System] Updating the system..."
apt update &> /dev/null

# Install Java
echo "[Info] [Java] Installing JDK"
apt install default-jdk -y &> /dev/null

# Setup python3
echo "[Info] [Python] Installing pip3..."
apt install -y python3-pip &> /dev/null

# Install jupyter
echo "[Info] [Python] Installing jupyter..."
pip3 install jupyter &> /dev/null

# Install Spark
echo "[Info] [Spark] Installing SPARK..."
wget https://downloads.apache.org/spark/spark-3.2.4/spark-3.2.4-bin-hadoop2.7.tgz &> /dev/null

tar -xzf spark-3.2.4-bin-hadoop2.7.tgz
mv spark-3.2.4-bin-hadoop2.7 /usr/local/spark
