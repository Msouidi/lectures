echo "[Info] [Spark] Starting spark..."
export  SPARK_HOME=/usr/local/spark; \
export PATH=$SPARK_HOME/bin:$PATH; \
export PYSPARK_DRIVER_PYTHON=jupyter; \
export PYSPARK_DRIVER_PYTHON_OPTS="notebook --ip=0.0.0.0 --allow-root --NotebookApp.token='' --NotebookApp.password=''"; \
export PATH=$PATH:~/.local/bin; \
pyspark &
echo "[Info] [Spark] Runing spark http://192.168.33.12:8888"